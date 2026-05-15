from datetime import datetime, timedelta, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_
import io
import openpyxl
from database import get_db
from models import Order, OrderStatusHistory, Driver, Vehicle, User, CommonAddress
from schemas import (
    OrderCreate, OrderReject, OrderAssign, OrderOut, StatusHistoryOut,
)
from auth import require_role, get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


def _build_order_out(o: Order) -> OrderOut:
    return OrderOut(
        id=o.id,
        employee_id=o.employee_id,
        employee_name=o.employee.full_name if o.employee else None,
        driver_id=o.driver_id,
        driver_name=o.driver.full_name if o.driver else None,
        vehicle_id=o.vehicle_id,
        vehicle_info=f"{o.vehicle.make} {o.vehicle.model} ({o.vehicle.license_plate})" if o.vehicle else None,
        departure_address=o.departure_address,
        destination_address=o.destination_address,
        desired_datetime=o.desired_datetime,
        expected_duration_minutes=o.expected_duration_minutes,
        purpose=o.purpose,
        notes=o.notes,
        status=o.status,
        rejection_reason=o.rejection_reason,
        actual_departure=o.actual_departure,
        actual_return=o.actual_return,
        created_at=o.created_at,
        status_history=[
            StatusHistoryOut(
                id=h.id,
                old_status=h.old_status,
                new_status=h.new_status,
                comment=h.comment,
                changed_at=h.changed_at,
            )
            for h in o.status_history
        ],
    )


def _add_history(db: Session, order: Order, new_status: str, user: User, comment: str = None):
    h = OrderStatusHistory(
        order_id=order.id,
        old_status=order.status,
        new_status=new_status,
        changed_by=user.id,
        comment=comment,
    )
    db.add(h)
    order.status = new_status


def _check_driver_available(db, driver_id, start, duration_min, exclude_id=None):
    end = start + timedelta(minutes=duration_min)
    q = db.query(Order).filter(
        Order.driver_id == driver_id,
        Order.status.in_(["accepted", "in_progress"]),
        Order.desired_datetime < end,
        (Order.desired_datetime + timedelta(minutes=duration_min)) > start,
    )
    if exclude_id:
        q = q.filter(Order.id != exclude_id)
    return q.first()


def _check_vehicle_available(db, vehicle_id, start, duration_min, exclude_id=None):
    end = start + timedelta(minutes=duration_min)
    q = db.query(Order).filter(
        Order.vehicle_id == vehicle_id,
        Order.status.in_(["accepted", "in_progress"]),
        Order.desired_datetime < end,
        (Order.desired_datetime + timedelta(minutes=duration_min)) > start,
    )
    if exclude_id:
        q = q.filter(Order.id != exclude_id)
    return q.first()


# ── Employee ──────────────────────────────────────────────────────────────────

@router.post("/", response_model=OrderOut)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("employee")),
):
    o = Order(employee_id=current_user.id, **data.model_dump())
    db.add(o)
    db.flush()
    db.add(OrderStatusHistory(order_id=o.id, new_status="new",
                              changed_by=current_user.id, comment="Заявка создана"))
    for addr in [data.departure_address, data.destination_address]:
        ca = db.query(CommonAddress).filter(CommonAddress.address == addr).first()
        if ca:
            ca.usage_count += 1
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


@router.get("/my", response_model=List[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("employee")),
):
    orders = (
        db.query(Order)
        .filter(Order.employee_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_build_order_out(o) for o in orders]


@router.delete("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("employee")),
):
    o = db.query(Order).filter(Order.id == order_id,
                               Order.employee_id == current_user.id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if o.status != "new":
        raise HTTPException(status_code=400,
                            detail="Отменить можно только заявку в статусе 'новая'")
    _add_history(db, o, "cancelled", current_user, "Отменено сотрудником")
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


# ── Driver (объявляем ДО /{order_id}, чтобы FastAPI не спутал маршруты) ───────

@router.get("/driver/assignments", response_model=List[OrderOut])
def driver_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("driver")),
):
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Профиль водителя не найден. Обратитесь к диспетчеру.",
        )
    orders = (
        db.query(Order)
        .filter(Order.driver_id == driver.id,
                Order.status.in_(["in_progress", "completed"]))
        .order_by(Order.desired_datetime.desc())
        .all()
    )
    return [_build_order_out(o) for o in orders]


@router.post("/{order_id}/depart", response_model=OrderOut)
def mark_departure(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("driver")),
):
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Профиль водителя не найден")
    o = db.query(Order).filter(Order.id == order_id,
                               Order.driver_id == driver.id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if o.status != "in_progress":
        raise HTTPException(status_code=400,
                            detail="Заявка не в статусе 'выполняется'")
    o.actual_departure = datetime.now(timezone.utc)
    db.add(OrderStatusHistory(order_id=o.id, old_status=o.status,
                              new_status=o.status, changed_by=current_user.id,
                              comment="Водитель выехал"))
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


@router.post("/{order_id}/return", response_model=OrderOut)
def mark_return(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("driver")),
):
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Профиль водителя не найден")
    o = db.query(Order).filter(Order.id == order_id,
                               Order.driver_id == driver.id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if o.status != "in_progress":
        raise HTTPException(status_code=400,
                            detail="Заявка не в статусе 'выполняется'")
    o.actual_return = datetime.now(timezone.utc)
    _add_history(db, o, "completed", current_user, "Водитель вернулся, поездка завершена")
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


# ── Dispatcher ────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[OrderOut])
def list_orders(
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    driver_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    q = db.query(Order)
    if status:
        q = q.filter(Order.status == status)
    if date_from:
        q = q.filter(Order.desired_datetime >= date_from)
    if date_to:
        q = q.filter(Order.desired_datetime <= date_to)
    if driver_id:
        q = q.filter(Order.driver_id == driver_id)
    return [_build_order_out(o) for o in q.order_by(Order.created_at.desc())
            .offset(skip).limit(limit).all()]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    role = current_user.role.name
    if role == "employee" and o.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    # Водитель может видеть только свои заявки
    if role == "driver":
        driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
        if not driver or o.driver_id != driver.id:
            raise HTTPException(status_code=403, detail="Нет доступа")
    return _build_order_out(o)


@router.post("/{order_id}/accept", response_model=OrderOut)
def accept_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if o.status != "new":
        raise HTTPException(status_code=400, detail="Принять можно только новую заявку")
    _add_history(db, o, "accepted", current_user, "Принято диспетчером")
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


@router.post("/{order_id}/reject", response_model=OrderOut)
def reject_order(
    order_id: int,
    data: OrderReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    if not data.rejection_reason or not data.rejection_reason.strip():
        raise HTTPException(status_code=400,
                            detail="Укажите причину отклонения заявки")
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if o.status not in ("new", "accepted"):
        raise HTTPException(status_code=400,
                            detail="Нельзя отклонить заявку в текущем статусе")
    o.rejection_reason = data.rejection_reason.strip()
    _add_history(db, o, "rejected", current_user,
                 f"Отклонено: {data.rejection_reason}")
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


@router.post("/{order_id}/assign", response_model=OrderOut)
def assign_order(
    order_id: int,
    data: OrderAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    # Валидация: водитель и машина обязательны
    if not data.driver_id:
        raise HTTPException(status_code=400, detail="Необходимо выбрать водителя")
    if not data.vehicle_id:
        raise HTTPException(status_code=400, detail="Необходимо выбрать автомобиль")

    o = db.query(Order).filter(Order.id == order_id).with_for_update().first()
    if not o:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if o.status != "accepted":
        raise HTTPException(status_code=400,
                            detail="Назначить можно только принятую заявку")

    driver = db.query(Driver).filter(Driver.id == data.driver_id,
                                     Driver.status == "active").first()
    if not driver:
        raise HTTPException(status_code=404,
                            detail="Водитель не найден или неактивен")

    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id,
                                       Vehicle.status == "active").first()
    if not vehicle:
        raise HTTPException(status_code=404,
                            detail="Автомобиль не найден или неактивен")

    duration = data.expected_duration_minutes or o.expected_duration_minutes

    conflict_d = _check_driver_available(db, data.driver_id,
                                         o.desired_datetime, duration, order_id)
    if conflict_d:
        raise HTTPException(
            status_code=409,
            detail=f"Водитель занят: заявка #{conflict_d.id} пересекается по времени",
        )

    conflict_v = _check_vehicle_available(db, data.vehicle_id,
                                           o.desired_datetime, duration, order_id)
    if conflict_v:
        raise HTTPException(
            status_code=409,
            detail=f"Автомобиль занят: заявка #{conflict_v.id} пересекается по времени",
        )

    o.driver_id = data.driver_id
    o.vehicle_id = data.vehicle_id
    if data.expected_duration_minutes:
        o.expected_duration_minutes = data.expected_duration_minutes

    _add_history(db, o, "in_progress", current_user,
                 f"Назначен водитель {driver.full_name}, авто {vehicle.license_plate}")
    db.commit()
    db.refresh(o)
    return _build_order_out(o)


# ── Export ────────────────────────────────────────────────────────────────────

@router.get("/export/excel")
def export_excel(
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    driver_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    q = db.query(Order)
    if status:
        q = q.filter(Order.status == status)
    if date_from:
        q = q.filter(Order.desired_datetime >= date_from)
    if date_to:
        q = q.filter(Order.desired_datetime <= date_to)
    if driver_id:
        q = q.filter(Order.driver_id == driver_id)
    orders = q.order_by(Order.desired_datetime.desc()).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "История поездок"
    ws.append(["ID", "Сотрудник", "Водитель", "Автомобиль", "Откуда", "Куда",
               "Дата/время", "Цель", "Статус", "Время выезда", "Время возврата"])
    for o in orders:
        ws.append([
            o.id,
            o.employee.full_name if o.employee else "",
            o.driver.full_name if o.driver else "",
            f"{o.vehicle.make} {o.vehicle.model} ({o.vehicle.license_plate})" if o.vehicle else "",
            o.departure_address,
            o.destination_address,
            o.desired_datetime.strftime("%d.%m.%Y %H:%M") if o.desired_datetime else "",
            o.purpose,
            o.status,
            o.actual_departure.strftime("%d.%m.%Y %H:%M") if o.actual_departure else "",
            o.actual_return.strftime("%d.%m.%Y %H:%M") if o.actual_return else "",
        ])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=history.xlsx"},
    )

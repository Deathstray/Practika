from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import CommonAddress, Order, Driver, User
from schemas import (
    CommonAddressCreate, CommonAddressUpdate, CommonAddressOut,
    DashboardStats, StatsOut, DriverLoad, TopRoute, DailyCount,
)
from auth import require_role, get_current_user
from routers.orders import _build_order_out

addr_router = APIRouter(prefix="/addresses", tags=["addresses"])
stats_router = APIRouter(prefix="/stats", tags=["stats"])


@addr_router.get("/", response_model=List[CommonAddressOut])
def list_addresses(
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(CommonAddress).filter(CommonAddress.is_active == True)
    if q:
        query = query.filter(CommonAddress.address.ilike(f"%{q}%"))
    return query.order_by(CommonAddress.usage_count.desc()).limit(20).all()


@addr_router.post("/", response_model=CommonAddressOut)
def create_address(
    data: CommonAddressCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    if db.query(CommonAddress).filter(CommonAddress.address == data.address).first():
        raise HTTPException(status_code=400, detail="Адрес уже существует")
    a = CommonAddress(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@addr_router.patch("/{addr_id}", response_model=CommonAddressOut)
def update_address(
    addr_id: int,
    data: CommonAddressUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    a = db.query(CommonAddress).filter(CommonAddress.id == addr_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(a, field, value)
    db.commit()
    db.refresh(a)
    return a


@addr_router.delete("/{addr_id}", response_model=CommonAddressOut)
def delete_address(
    addr_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    a = db.query(CommonAddress).filter(CommonAddress.id == addr_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    a.is_active = False
    db.commit()
    db.refresh(a)
    return a


@stats_router.get("/dashboard", response_model=DashboardStats)
def dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    active_orders = db.query(Order).filter(Order.status == "in_progress").all()
    free_drivers = db.query(Driver).filter(
        Driver.status == "active",
        ~Driver.id.in_(
            db.query(Order.driver_id).filter(Order.status == "in_progress", Order.driver_id != None)
        )
    ).count()
    new_orders = db.query(Order).filter(Order.status == "new").count()

    return DashboardStats(
        active_trips=len(active_orders),
        free_drivers=free_drivers,
        new_orders=new_orders,
        active_orders=[_build_order_out(o) for o in active_orders],
    )


@stats_router.get("/", response_model=StatsOut)
def statistics(
    date_from: datetime = Query(...),
    date_to: datetime = Query(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    orders = db.query(Order).filter(
        Order.desired_datetime >= date_from,
        Order.desired_datetime <= date_to,
    ).all()

    total = len(orders)
    completed = sum(1 for o in orders if o.status == "completed")

    from collections import Counter
    route_counter = Counter(
        f"{o.departure_address} -> {o.destination_address}" for o in orders
    )
    top_routes = [TopRoute(route=r, count=c) for r, c in route_counter.most_common(5)]

    driver_counter = Counter(
        o.driver.full_name for o in orders if o.driver and o.status == "completed"
    )
    driver_loads = [DriverLoad(driver_name=n, completed=c) for n, c in driver_counter.most_common()]

    day_counter = Counter(
        o.desired_datetime.strftime("%Y-%m-%d") for o in orders
    )
    daily_counts = []
    current = date_from.date()
    end_date = date_to.date()
    while current <= end_date:
        key = current.strftime("%Y-%m-%d")
        daily_counts.append(DailyCount(date=key, count=day_counter.get(key, 0)))
        current += timedelta(days=1)

    return StatsOut(
        total_orders=total,
        completed_orders=completed,
        top_routes=top_routes,
        driver_loads=driver_loads,
        daily_counts=daily_counts,
    )

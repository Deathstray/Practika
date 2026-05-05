from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Driver, User
from schemas import DriverCreate, DriverUpdate, DriverOut
from auth import require_role, get_current_user

router = APIRouter(prefix="/drivers", tags=["drivers"])


def _to_out(d: Driver) -> DriverOut:
    return DriverOut(
        id=d.id,
        full_name=d.full_name,
        employee_number=d.employee_number,
        phone=d.phone,
        license_number=d.license_number,
        status=d.status,
        user_id=d.user_id,
        created_at=d.created_at,
    )


@router.get("/", response_model=list[DriverOut])
def list_drivers(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(Driver)
    if status:
        q = q.filter(Driver.status == status)
    return [_to_out(d) for d in q.order_by(Driver.full_name).all()]


@router.post("/", response_model=DriverOut)
def create_driver(
    data: DriverCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    if db.query(Driver).filter(Driver.employee_number == data.employee_number).first():
        raise HTTPException(status_code=400, detail="Табельный номер уже занят")
    d = Driver(**data.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return _to_out(d)


@router.get("/{driver_id}", response_model=DriverOut)
def get_driver(driver_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    d = db.query(Driver).filter(Driver.id == driver_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Водитель не найден")
    return _to_out(d)


@router.patch("/{driver_id}", response_model=DriverOut)
def update_driver(
    driver_id: int,
    data: DriverUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    d = db.query(Driver).filter(Driver.id == driver_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Водитель не найден")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(d, field, value)
    db.commit()
    db.refresh(d)
    return _to_out(d)


@router.delete("/{driver_id}", response_model=DriverOut)
def deactivate_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    d = db.query(Driver).filter(Driver.id == driver_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Водитель не найден")
    d.status = "inactive"
    db.commit()
    db.refresh(d)
    return _to_out(d)

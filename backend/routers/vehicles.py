from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vehicle, User
from schemas import VehicleCreate, VehicleUpdate, VehicleOut
from auth import require_role, get_current_user

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def _to_out(v: Vehicle) -> VehicleOut:
    return VehicleOut(
        id=v.id,
        make=v.make,
        model=v.model,
        license_plate=v.license_plate,
        vehicle_type=v.vehicle_type,
        capacity=v.capacity,
        status=v.status,
        created_at=v.created_at,
    )


@router.get("/", response_model=list[VehicleOut])
def list_vehicles(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(Vehicle)
    if status:
        q = q.filter(Vehicle.status == status)
    return [_to_out(v) for v in q.order_by(Vehicle.make).all()]


@router.post("/", response_model=VehicleOut)
def create_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    if db.query(Vehicle).filter(Vehicle.license_plate == data.license_plate).first():
        raise HTTPException(status_code=400, detail="Гос. номер уже существует")
    v = Vehicle(**data.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    return _to_out(v)


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    v = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")
    return _to_out(v)


@router.patch("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    v = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(v, field, value)
    db.commit()
    db.refresh(v)
    return _to_out(v)


@router.delete("/{vehicle_id}", response_model=VehicleOut)
def deactivate_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("dispatcher")),
):
    v = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")
    v.status = "inactive"
    db.commit()
    db.refresh(v)
    return _to_out(v)

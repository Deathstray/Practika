from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    full_name: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str  # employee | dispatcher | driver

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ("employee", "dispatcher", "driver"):
            raise ValueError("Допустимые роли: employee, dispatcher, driver")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Drivers ───────────────────────────────────────────────────────────────────

class DriverCreate(BaseModel):
    full_name: str
    employee_number: str
    phone: Optional[str] = None
    license_number: Optional[str] = None
    user_id: Optional[int] = None

class DriverUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[int] = None

class DriverOut(BaseModel):
    id: int
    full_name: str
    employee_number: str
    phone: Optional[str]
    license_number: Optional[str]
    status: str
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Vehicles ──────────────────────────────────────────────────────────────────

class VehicleCreate(BaseModel):
    make: str
    model: str
    license_plate: str
    vehicle_type: str
    capacity: Optional[int] = None

class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    license_plate: Optional[str] = None
    vehicle_type: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None

class VehicleOut(BaseModel):
    id: int
    make: str
    model: str
    license_plate: str
    vehicle_type: str
    capacity: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Orders ────────────────────────────────────────────────────────────────────

class OrderCreate(BaseModel):
    departure_address: str
    destination_address: str
    desired_datetime: datetime
    expected_duration_minutes: int = 60
    purpose: str
    notes: Optional[str] = None

class OrderReject(BaseModel):
    rejection_reason: str

class OrderAssign(BaseModel):
    driver_id: int
    vehicle_id: int
    expected_duration_minutes: Optional[int] = None

class StatusHistoryOut(BaseModel):
    id: int
    old_status: Optional[str]
    new_status: str
    comment: Optional[str]
    changed_at: datetime

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    driver_id: Optional[int]
    driver_name: Optional[str] = None
    vehicle_id: Optional[int]
    vehicle_info: Optional[str] = None
    departure_address: str
    destination_address: str
    desired_datetime: datetime
    expected_duration_minutes: int
    purpose: str
    notes: Optional[str]
    status: str
    rejection_reason: Optional[str]
    actual_departure: Optional[datetime]
    actual_return: Optional[datetime]
    created_at: datetime
    status_history: List[StatusHistoryOut] = []

    class Config:
        from_attributes = True


# ── Common Addresses ──────────────────────────────────────────────────────────

class CommonAddressCreate(BaseModel):
    address: str
    label: Optional[str] = None

class CommonAddressUpdate(BaseModel):
    address: Optional[str] = None
    label: Optional[str] = None
    is_active: Optional[bool] = None

class CommonAddressOut(BaseModel):
    id: int
    address: str
    label: Optional[str]
    usage_count: int
    is_active: bool

    class Config:
        from_attributes = True


# ── Stats ─────────────────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    active_trips: int
    free_drivers: int
    new_orders: int
    active_orders: List[OrderOut]

class StatsRequest(BaseModel):
    date_from: datetime
    date_to: datetime

class DriverLoad(BaseModel):
    driver_name: str
    completed: int

class TopRoute(BaseModel):
    route: str
    count: int

class DailyCount(BaseModel):
    date: str
    count: int

class StatsOut(BaseModel):
    total_orders: int
    completed_orders: int
    top_routes: List[TopRoute]
    driver_loads: List[DriverLoad]
    daily_counts: List[DailyCount]

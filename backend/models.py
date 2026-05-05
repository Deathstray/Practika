from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey,
    DateTime, func, CheckConstraint
)
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(200), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    role = relationship("Role", back_populates="users")
    orders = relationship("Order", back_populates="employee", foreign_keys="Order.employee_id")
    driver_profile = relationship("Driver", back_populates="user", uselist=False)


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    full_name = Column(String(200), nullable=False)
    employee_number = Column(String(50), nullable=False, unique=True)
    phone = Column(String(30))
    license_number = Column(String(50))
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="driver_profile")
    orders = relationship("Order", back_populates="driver")

    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive')", name="ck_driver_status"),
    )


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    license_plate = Column(String(20), nullable=False, unique=True)
    vehicle_type = Column(String(50), nullable=False)
    capacity = Column(Integer)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="vehicle")

    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive')", name="ck_vehicle_status"),
    )


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    departure_address = Column(String(500), nullable=False)
    destination_address = Column(String(500), nullable=False)
    desired_datetime = Column(DateTime(timezone=True), nullable=False)
    expected_duration_minutes = Column(Integer, nullable=False, default=60)
    purpose = Column(String(500), nullable=False)
    notes = Column(Text)
    status = Column(String(30), nullable=False, default="new")
    rejection_reason = Column(Text)
    actual_departure = Column(DateTime(timezone=True))
    actual_return = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    employee = relationship("User", back_populates="orders", foreign_keys=[employee_id])
    driver = relationship("Driver", back_populates="orders")
    vehicle = relationship("Vehicle", back_populates="orders")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint(
            "status IN ('new','accepted','rejected','in_progress','completed','cancelled')",
            name="ck_order_status"
        ),
    )


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String(30))
    new_status = Column(String(30), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"))
    comment = Column(Text)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="status_history")
    user = relationship("User")


class CommonAddress(Base):
    __tablename__ = "common_addresses"
    id = Column(Integer, primary_key=True)
    address = Column(String(500), nullable=False, unique=True)
    label = Column(String(200))
    usage_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

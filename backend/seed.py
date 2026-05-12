from sqlalchemy.orm import Session

from auth import hash_password
from models import CommonAddress, Driver, Role, User, Vehicle


DEFAULT_PASSWORD = "admin123"


def _get_or_create_role(db: Session, name: str, description: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role:
        return role
    role = Role(name=name, description=description)
    db.add(role)
    db.flush()
    return role


def _get_or_create_user(
    db: Session,
    *,
    username: str,
    email: str,
    full_name: str,
    role: Role,
    password: str = DEFAULT_PASSWORD,
) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        role_id=role.id,
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


def seed_database(db: Session) -> None:
    employee_role = _get_or_create_role(db, "employee", "Сотрудник — подаёт заявки на транспорт")
    dispatcher_role = _get_or_create_role(db, "dispatcher", "Диспетчер — управляет заявками и назначает транспорт")
    driver_role = _get_or_create_role(db, "driver", "Водитель — выполняет поездки")

    _get_or_create_user(
        db,
        username="dispatcher",
        email="dispatcher@company.ru",
        full_name="Главный диспетчер",
        role=dispatcher_role,
    )
    _get_or_create_user(
        db,
        username="employee1",
        email="employee1@company.ru",
        full_name="Иванов Иван Иванович",
        role=employee_role,
    )
    driver_user = _get_or_create_user(
        db,
        username="driver1",
        email="driver1@company.ru",
        full_name="Петров Пётр Петрович",
        role=driver_role,
    )

    # Создаём карточку водителя и ВСЕГДА обновляем user_id
    # (на случай если БД старая и user_id не был привязан)
    existing_driver = db.query(Driver).filter(Driver.employee_number == "DRV-001").first()
    if not existing_driver:
        db.add(
            Driver(
                user_id=driver_user.id,
                full_name="Петров Пётр Петрович",
                employee_number="DRV-001",
                phone="+7-999-111-22-33",
                license_number="АА 123456",
                status="active",
            )
        )
        db.flush()
    else:
        # Исправляем user_id если слетел при пересборке
        if existing_driver.user_id != driver_user.id:
            existing_driver.user_id = driver_user.id

    for make, model, plate, vehicle_type, capacity in [
        ("Toyota", "Camry", "А123БВ77", "sedan", 4),
        ("Ford", "Transit", "В456ГД77", "minibus", 12),
        ("Lada", "Vesta", "Е789ЖЗ77", "sedan", 4),
    ]:
        if not db.query(Vehicle).filter(Vehicle.license_plate == plate).first():
            db.add(
                Vehicle(
                    make=make,
                    model=model,
                    license_plate=plate,
                    vehicle_type=vehicle_type,
                    capacity=capacity,
                    status="active",
                )
            )

    for address, label in [
        ("ул. Ленина, 1, Москва", "Главный офис"),
        ("Красная площадь, 1, Москва", "Администрация"),
        ("ул. Тверская, 13, Москва", "Партнёр"),
        ("Домодедово аэропорт, Москва", "Аэропорт Домодедово"),
        ("Шереметьево аэропорт, Москва", "Аэропорт Шереметьево"),
    ]:
        if not db.query(CommonAddress).filter(CommonAddress.address == address).first():
            db.add(CommonAddress(address=address, label=label, usage_count=0, is_active=True))

    db.commit()

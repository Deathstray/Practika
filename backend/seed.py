"""
Начальные данные БД.
Запускается отдельной командой: python seed.py
Использует блокировку на уровне БД — безопасен при нескольких воркерах.
"""
import logging
from sqlalchemy import text
from database import SessionLocal, engine
from models import Base, Role, User, Driver, Vehicle, CommonAddress
from auth import hash_password

logger = logging.getLogger(__name__)

ADVISORY_LOCK_ID = 987654321  # произвольный уникальный int для pg_advisory_lock


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        is_sqlite = "sqlite" in str(engine.url)

        if not is_sqlite:
            # PostgreSQL: блокировка на уровне БД — только один воркер выполнит seed
            db.execute(text(f"SELECT pg_advisory_lock({ADVISORY_LOCK_ID})"))

        try:
            if db.query(Role).count() > 0:
                logger.info("База данных уже заполнена, пропускаем seed.")
                return

            logger.info("Заполняю базу данных начальными данными...")

            role_employee   = Role(name="employee",   description="Сотрудник")
            role_dispatcher = Role(name="dispatcher", description="Диспетчер")
            role_driver     = Role(name="driver",     description="Водитель")
            db.add_all([role_employee, role_dispatcher, role_driver])
            db.flush()

            hashed = hash_password("admin123")

            user_dispatcher = User(
                username="dispatcher", email="dispatcher@company.ru",
                hashed_password=hashed, full_name="Главный диспетчер",
                role_id=role_dispatcher.id,
            )
            user_employee = User(
                username="employee1", email="employee1@company.ru",
                hashed_password=hashed, full_name="Иванов Иван Иванович",
                role_id=role_employee.id,
            )
            user_driver = User(
                username="driver1", email="driver1@company.ru",
                hashed_password=hashed, full_name="Петров Пётр Петрович",
                role_id=role_driver.id,
            )
            db.add_all([user_dispatcher, user_employee, user_driver])
            db.flush()

            db.add(Driver(
                full_name="Петров Пётр Петрович",
                employee_number="DRV-001",
                phone="+7-999-111-22-33",
                license_number="АА 123456",
                status="active",
                user_id=user_driver.id,
            ))

            db.add_all([
                Vehicle(make="Toyota", model="Camry",   license_plate="А123БВ77", vehicle_type="sedan",   capacity=4,  status="active"),
                Vehicle(make="Ford",   model="Transit", license_plate="В456ГД77", vehicle_type="minibus", capacity=12, status="active"),
                Vehicle(make="Lada",   model="Vesta",   license_plate="Е789ЖЗ77", vehicle_type="sedan",   capacity=4,  status="active"),
            ])

            db.add_all([
                CommonAddress(address="ул. Ленина, 1, Москва",        label="Главный офис"),
                CommonAddress(address="Красная площадь, 1, Москва",   label="Администрация"),
                CommonAddress(address="ул. Тверская, 13, Москва",     label="Партнёр"),
                CommonAddress(address="Домодедово аэропорт, Москва",  label="Аэропорт Домодедово"),
                CommonAddress(address="Шереметьево аэропорт, Москва", label="Аэропорт Шереметьево"),
            ])

            db.commit()
            logger.info("База данных успешно заполнена.")

        finally:
            if not is_sqlite:
                db.execute(text(f"SELECT pg_advisory_unlock({ADVISORY_LOCK_ID})"))

    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка заполнения БД: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed()

"""
Создаёт таблицы и заполняет БД начальными данными.
Запускается автоматически при старте приложения.
"""
from database import SessionLocal, engine
from models import Base, Role, User, Driver, Vehicle, CommonAddress
from auth import hash_password


def seed():
    # Создаём все таблицы (если ещё не созданы)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Если роли уже есть — данные уже залиты, выходим
        if db.query(Role).count() > 0:
            return

        print("⏳ Заполняю базу данных начальными данными...")

        # Роли
        role_employee   = Role(name="employee",   description="Сотрудник — подаёт заявки на транспорт")
        role_dispatcher = Role(name="dispatcher", description="Диспетчер — управляет заявками")
        role_driver     = Role(name="driver",     description="Водитель — выполняет поездки")
        db.add_all([role_employee, role_dispatcher, role_driver])
        db.flush()  # получаем id до commit

        # Пользователи (пароль: admin123)
        hashed = hash_password("admin123")
        db.add_all([
            User(username="dispatcher", email="dispatcher@company.ru",
                 hashed_password=hashed, full_name="Главный диспетчер",
                 role_id=role_dispatcher.id),
            User(username="employee1", email="employee1@company.ru",
                 hashed_password=hashed, full_name="Иванов Иван Иванович",
                 role_id=role_employee.id),
            User(username="driver1", email="driver1@company.ru",
                 hashed_password=hashed, full_name="Петров Пётр Петрович",
                 role_id=role_driver.id),
        ])

        # Водитель
        db.add(Driver(
            full_name="Петров Пётр Петрович",
            employee_number="DRV-001",
            phone="+7-999-111-22-33",
            license_number="АА 123456",
            status="active",
        ))

        # Автомобили
        db.add_all([
            Vehicle(make="Toyota", model="Camry",   license_plate="А123БВ77", vehicle_type="sedan",   capacity=4,  status="active"),
            Vehicle(make="Ford",   model="Transit", license_plate="В456ГД77", vehicle_type="minibus", capacity=12, status="active"),
            Vehicle(make="Lada",   model="Vesta",   license_plate="Е789ЖЗ77", vehicle_type="sedan",   capacity=4,  status="active"),
        ])

        # Популярные адреса
        db.add_all([
            CommonAddress(address="ул. Ленина, 1, Москва",          label="Главный офис"),
            CommonAddress(address="Красная площадь, 1, Москва",     label="Администрация"),
            CommonAddress(address="ул. Тверская, 13, Москва",       label="Партнёр"),
            CommonAddress(address="Домодедово аэропорт, Москва",    label="Аэропорт Домодедово"),
            CommonAddress(address="Шереметьево аэропорт, Москва",   label="Аэропорт Шереметьево"),
        ])

        db.commit()
        print("✅ База данных успешно заполнена!")
        print("   Логины: dispatcher / employee1 / driver1")
        print("   Пароль: admin123")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка заполнения БД: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()

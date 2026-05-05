-- ================================================================
-- Система диспетчеризации служебного транспорта
-- Полная схема БД
-- ================================================================

-- Справочник ролей
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);

INSERT INTO roles (name, description) VALUES
    ('employee', 'Сотрудник — подаёт заявки на транспорт'),
    ('dispatcher', 'Диспетчер — управляет заявками и назначает транспорт'),
    ('driver', 'Водитель — выполняет поездки')
ON CONFLICT (name) DO NOTHING;

-- Пользователи
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(200) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);

-- Водители
CREATE TABLE IF NOT EXISTS drivers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    full_name VARCHAR(200) NOT NULL,
    employee_number VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(30),
    license_number VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_drivers_status ON drivers(status);
CREATE INDEX IF NOT EXISTS idx_drivers_employee_number ON drivers(employee_number);

-- Транспортные средства
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    license_plate VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(50) NOT NULL,
    capacity INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status);
CREATE INDEX IF NOT EXISTS idx_vehicles_license_plate ON vehicles(license_plate);

-- Заявки на транспорт
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES users(id),
    driver_id INTEGER REFERENCES drivers(id),
    vehicle_id INTEGER REFERENCES vehicles(id),
    departure_address VARCHAR(500) NOT NULL,
    destination_address VARCHAR(500) NOT NULL,
    desired_datetime TIMESTAMPTZ NOT NULL,
    expected_duration_minutes INTEGER NOT NULL DEFAULT 60,
    purpose VARCHAR(500) NOT NULL,
    notes TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'accepted', 'rejected', 'in_progress', 'completed', 'cancelled')),
    rejection_reason TEXT,
    actual_departure TIMESTAMPTZ,
    actual_return TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orders_employee_id ON orders(employee_id);
CREATE INDEX IF NOT EXISTS idx_orders_driver_id ON orders(driver_id);
CREATE INDEX IF NOT EXISTS idx_orders_vehicle_id ON orders(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_desired_datetime ON orders(desired_datetime);

-- История статусов заявки
CREATE TABLE IF NOT EXISTS order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    old_status VARCHAR(30),
    new_status VARCHAR(30) NOT NULL,
    changed_by INTEGER REFERENCES users(id),
    comment TEXT,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_order_status_history_order_id ON order_status_history(order_id);

-- Справочник часто используемых адресов
CREATE TABLE IF NOT EXISTS common_addresses (
    id SERIAL PRIMARY KEY,
    address VARCHAR(500) NOT NULL UNIQUE,
    label VARCHAR(200),
    usage_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_common_addresses_address ON common_addresses USING gin(to_tsvector('russian', address));

-- Начальные данные: администратор-диспетчер
-- Пароль: admin123 (bcrypt hash)
INSERT INTO users (username, email, hashed_password, full_name, role_id)
SELECT 'dispatcher', 'dispatcher@company.ru',
       '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
       'Главный диспетчер', r.id
FROM roles r WHERE r.name = 'dispatcher'
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, hashed_password, full_name, role_id)
SELECT 'employee1', 'employee1@company.ru',
       '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
       'Иванов Иван Иванович', r.id
FROM roles r WHERE r.name = 'employee'
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, hashed_password, full_name, role_id)
SELECT 'driver1', 'driver1@company.ru',
       '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
       'Петров Пётр Петрович', r.id
FROM roles r WHERE r.name = 'driver'
ON CONFLICT (username) DO NOTHING;

-- Тестовый водитель
INSERT INTO drivers (full_name, employee_number, phone, license_number, status)
VALUES ('Петров Пётр Петрович', 'DRV-001', '+7-999-111-22-33', 'АА 123456', 'active')
ON CONFLICT (employee_number) DO NOTHING;

-- Тестовые машины
INSERT INTO vehicles (make, model, license_plate, vehicle_type, capacity, status) VALUES
    ('Toyota', 'Camry', 'А123БВ77', 'sedan', 4, 'active'),
    ('Ford', 'Transit', 'В456ГД77', 'minibus', 12, 'active'),
    ('Lada', 'Vesta', 'Е789ЖЗ77', 'sedan', 4, 'active')
ON CONFLICT (license_plate) DO NOTHING;

-- Популярные адреса
INSERT INTO common_addresses (address, label) VALUES
    ('ул. Ленина, 1, Москва', 'Главный офис'),
    ('Красная площадь, 1, Москва', 'Администрация'),
    ('ул. Тверская, 13, Москва', 'Партнёр'),
    ('Домодедово аэропорт, Москва', 'Аэропорт Домодедово'),
    ('Шереметьево аэропорт, Москва', 'Аэропорт Шереметьево')
ON CONFLICT (address) DO NOTHING;

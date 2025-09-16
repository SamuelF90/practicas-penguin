import sqlite3

def crear_base_de_datos():
    """
    Función principal para configurar la base de datos, crear las tablas
    e insertar datos de ejemplo.
    """
    print("Iniciando la creación de la base de datos...")
    
    # Crear conexión a SQLite. Si el archivo de BD no existe, se crea.
    conn = sqlite3.connect('hr_database.db')
    cursor = conn.cursor()

    # Habilitar soporte de FOREIGN KEY en SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Lista de tuplas con el nombre de la tabla y su sentencia SQL de creación
    tablas = [
        ("REGIONS", """
        CREATE TABLE IF NOT EXISTS regions (
            region_id       INTEGER     NOT NULL,
            region_name     VARCHAR(25),
            CONSTRAINT reg_id_pk PRIMARY KEY (region_id)
        );
        """),
        ("COUNTRIES", """
        CREATE TABLE IF NOT EXISTS countries (
            country_id      VARCHAR(2)  NOT NULL,
            country_name    VARCHAR(40),
            region_id       INTEGER,
            CONSTRAINT country_c_id_pk PRIMARY KEY (country_id),
            CONSTRAINT countr_reg_fk FOREIGN KEY (region_id) 
                REFERENCES regions(region_id)
        );
        """),
        ("LOCATIONS", """
        CREATE TABLE IF NOT EXISTS locations (
            location_id     INTEGER      NOT NULL,
            street_address  VARCHAR(40),
            postal_code     VARCHAR(12),
            city            VARCHAR(30)  NOT NULL,
            state_province  VARCHAR(25),
            country_id      VARCHAR(2),
            CONSTRAINT loc_id_pk PRIMARY KEY (location_id),
            CONSTRAINT loc_c_id_fk FOREIGN KEY (country_id) 
                REFERENCES countries(country_id)
        );
        """),
        ("JOBS", """
        CREATE TABLE IF NOT EXISTS jobs (
            job_id      VARCHAR(10) NOT NULL,
            job_title   VARCHAR(35) NOT NULL,
            min_salary  DECIMAL(6,0),
            max_salary  DECIMAL(6,0),
            CONSTRAINT job_id_pk PRIMARY KEY (job_id)
        );
        """),
        ("DEPARTMENTS", """
        CREATE TABLE IF NOT EXISTS departments (
            department_id   INTEGER      NOT NULL,
            department_name VARCHAR(30)  NOT NULL,
            manager_id      INTEGER,
            location_id     INTEGER,
            CONSTRAINT dept_id_pk PRIMARY KEY (department_id),
            CONSTRAINT dept_loc_fk FOREIGN KEY (location_id) 
                REFERENCES locations(location_id),
            CONSTRAINT dept_mgr_fk FOREIGN KEY (manager_id) 
                REFERENCES employees(employee_id)
        );
        """),
        ("EMPLOYEES", """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id     INTEGER      NOT NULL,
            first_name      VARCHAR(20),
            last_name       VARCHAR(25)  NOT NULL,
            email           VARCHAR(25)  NOT NULL,
            phone_number    VARCHAR(20),
            hire_date       DATE         NOT NULL,
            job_id          VARCHAR(10)  NOT NULL,
            salary          DECIMAL(8,2),
            commission_pct  DECIMAL(2,2),
            manager_id      INTEGER,
            department_id   INTEGER,
            CONSTRAINT emp_emp_id_pk PRIMARY KEY (employee_id),
            CONSTRAINT emp_email_uk UNIQUE (email),
            CONSTRAINT emp_salary_min CHECK (salary > 0),
            CONSTRAINT emp_job_fk FOREIGN KEY (job_id) 
                REFERENCES jobs(job_id),
            CONSTRAINT emp_dept_fk FOREIGN KEY (department_id) 
                REFERENCES departments(department_id),
            CONSTRAINT emp_manager_fk FOREIGN KEY (manager_id) 
                REFERENCES employees(employee_id)
        );
        """),
        ("JOB_HISTORY", """
        CREATE TABLE IF NOT EXISTS job_history (
            employee_id     INTEGER NOT NULL,
            start_date      DATE     NOT NULL,
            end_date        DATE     NOT NULL,
            job_id         VARCHAR(10) NOT NULL,
            department_id   INTEGER,
            CONSTRAINT jhist_emp_id_st_date_pk PRIMARY KEY (employee_id, start_date),
            CONSTRAINT jhist_date_interval CHECK (end_date > start_date),
            CONSTRAINT jhist_emp_fk FOREIGN KEY (employee_id) 
                REFERENCES employees(employee_id),
            CONSTRAINT jhist_job_fk FOREIGN KEY (job_id) 
                REFERENCES jobs(job_id),
            CONSTRAINT jhist_dept_fk FOREIGN KEY (department_id) 
                REFERENCES departments(department_id)
        );
        """)
    ]

    try:
        for nombre_tabla, sql_command in tablas:
            cursor.execute(sql_command)
            print(f"Tabla {nombre_tabla} creada exitosamente")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")
        conn.close()
        return

    # VERIFICAR TABLAS CREADAS
    def verificar_tablas(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_creadas = [row[0] for row in cursor.fetchall()]
        return tablas_creadas

    tablas_creadas = verificar_tablas(conn)
    print("\nTablas creadas:")
    for tabla in tablas_creadas:
        print(f"- {tabla}")
    
    # ------------------ INSERTS DE DATOS ------------------
    print("\nIniciando la inserción de datos de ejemplo...")

    # Insertar datos en REGIONS
    sql_insert_regions = """
    INSERT OR IGNORE INTO regions (region_id, region_name) VALUES 
    (1, 'Europe'),
    (2, 'Americas'),
    (3, 'Asia'),
    (4, 'Middle East and Africa');
    """
    cursor.execute(sql_insert_regions)
    conn.commit()
    print("Datos insertados en REGIONS")

    # Insertar datos en COUNTRIES
    sql_insert_countries = """
    INSERT OR IGNORE INTO countries (country_id, country_name, region_id) VALUES
    ('AR', 'Argentina', 2),
    ('AU', 'Australia', 3),
    ('BE', 'Belgium', 1),
    ('BR', 'Brazil', 2),
    ('CA', 'Canada', 2),
    ('CH', 'Switzerland', 1),
    ('CN', 'China', 3),
    ('DE', 'Germany', 1),
    ('DK', 'Denmark', 1),
    ('EG', 'Egypt', 4),
    ('FR', 'France', 1),
    ('IL', 'Israel', 4),
    ('IN', 'India', 3),
    ('IT', 'Italy', 1),
    ('JP', 'Japan', 3),
    ('MX', 'Mexico', 2),
    ('NG', 'Nigeria', 4),
    ('NL', 'Netherlands', 1),
    ('SG', 'Singapore', 3),
    ('UK', 'United Kingdom', 1),
    ('US', 'United States of America', 2),
    ('ZM', 'Zambia', 4),
    ('ZW', 'Zimbabwe', 4);
    """
    cursor.execute(sql_insert_countries)
    conn.commit()
    print("Datos insertados en COUNTRIES")

    # Insertar datos en LOCATIONS
    sql_insert_locations = """
    INSERT OR IGNORE INTO locations (location_id, street_address, postal_code, city, state_province, country_id) VALUES
    (1400, '2014 Jabberwocky Rd', '26192', 'Southlake', 'Texas', 'US'),
    (1500, '2011 Interiors Blvd', '99236', 'South San Francisco', 'California', 'US'),
    (1700, '2004 Charade Rd', '98199', 'Seattle', 'Washington', 'US'),
    (1800, '460 Bloor St. W.', 'ON M5S 1A8', 'Toronto', 'Ontario', 'CA'),
    (2500, 'Magdalen Centre, The Oxford Science Park', 'OX9 9ZB', 'Oxford', 'Oxford', 'UK');
    """
    cursor.execute(sql_insert_locations)
    conn.commit()
    print("Datos insertados en LOCATIONS")

    # Insertar datos en JOBS
    sql_insert_jobs = """
    INSERT OR IGNORE INTO jobs (job_id, job_title, min_salary, max_salary) VALUES
    ('AD_PRES', 'President', 20000, 40000),
    ('AD_VP', 'Administration Vice President', 15000, 30000),
    ('AD_ASST', 'Administration Assistant', 3000, 6000),
    ('IT_PROG', 'Programmer', 4000, 10000),
    ('SA_REP', 'Sales Representative', 6000, 12000),
    ('FI_MGR', 'Finance Manager', 8200, 16000),
    ('FI_ACCOUNT', 'Accountant', 4200, 9000),
    ('PU_MAN', 'Purchasing Manager', 8000, 15000),
    ('PU_CLERK', 'Purchasing Clerk', 2500, 5500),
    ('SH_CLERK', 'Shipping Clerk', 2500, 5500),
    ('ST_CLERK', 'Stock Clerk', 2000, 5000),
    ('SA_MAN', 'Sales Manager', 10000, 20000),
    ('MK_MAN', 'Marketing Manager', 13000, 20000),
    ('HR_REP', 'Human Resources Representative', 6500, 10000),
    ('PR_REP', 'Public Relations Representative', 10000, 15000),
    ('AC_MGR', 'Accounting Manager', 12000, 18000);
    """
    cursor.execute(sql_insert_jobs)
    conn.commit()
    print("Datos insertados en JOBS")

    # Insertar datos en DEPARTMENTS (temporalmente sin manager_id para evitar el error circular)
    sql_insert_departments = """
    INSERT OR IGNORE INTO departments (department_id, department_name, manager_id, location_id) VALUES
    (10, 'Administration', NULL, 1700),
    (20, 'Marketing', NULL, 1800),
    (30, 'Purchasing', NULL, 1700),
    (40, 'Human Resources', NULL, 2500),
    (50, 'Shipping', NULL, 1500),
    (60, 'IT', NULL, 1700),
    (70, 'Public Relations', NULL, 1700),
    (80, 'Sales', NULL, 2500),
    (90, 'Executive', NULL, 1700),
    (100, 'Finance', NULL, 1700),
    (110, 'Accounting', NULL, 1700);
    """
    cursor.execute(sql_insert_departments)
    conn.commit()
    print("Datos insertados en DEPARTMENTS (manager_id temporalmente nulo)")

    # Insertar datos en EMPLOYEES (ahora department_id ya existe)
    sql_insert_employees = """
    INSERT OR IGNORE INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id) VALUES
    (100, 'Steven', 'King', 'SKING', '515.123.4567', '2003-06-17', 'AD_PRES', 24000, NULL, NULL, 90),
    (101, 'Neena', 'Kochhar', 'NKOCHHAR', '515.123.4568', '2005-09-21', 'AD_VP', 17000, NULL, 100, 90),
    (102, 'Lex', 'De Haan', 'LDEHAAN', '515.123.4569', '2001-01-13', 'AD_VP', 17000, NULL, 100, 90),
    (103, 'Alexander', 'Hunold', 'AHUNOLD', '590.423.4567', '2006-01-03', 'IT_PROG', 9000, NULL, 102, 60),
    (104, 'Bruce', 'Ernst', 'BERNST', '590.423.4568', '2007-05-21', 'IT_PROG', 6000, NULL, 103, 60),
    (105, 'Diana', 'Lorentz', 'DLORENTZ', '590.423.5567', '2007-02-07', 'IT_PROG', 4200, NULL, 103, 60),
    (106, 'Valli', 'Pataballa', 'VPATABAL', '590.423.4569', '2006-02-05', 'IT_PROG', 4800, NULL, 103, 60),
    (107, 'Nancy', 'Greenberg', 'NGREENBE', '515.124.4569', '2002-08-17', 'FI_MGR', 12000, NULL, 101, 100),
    (108, 'Daniel', 'Faviet', 'DFAVIET', '515.124.4169', '2002-08-16', 'FI_ACCOUNT', 9000, NULL, 107, 100),
    (109, 'John', 'Chen', 'JCHEN', '515.124.4269', '2007-09-28', 'FI_ACCOUNT', 8200, NULL, 108, 100),
    (110, 'Ismael', 'Sciarra', 'ISCIARRA', '515.124.4369', '2005-09-30', 'FI_ACCOUNT', 7700, NULL, 108, 100),
    (111, 'Jose Manuel', 'Urman', 'JMURMAN', '515.124.4469', '2006-03-07', 'FI_ACCOUNT', 7800, NULL, 108, 100),
    (112, 'Luis', 'Popp', 'LPOPP', '515.124.4567', '2007-12-07', 'FI_ACCOUNT', 6900, NULL, 108, 100),
    (113, 'Karen', 'Colmenares', 'KCOLMENA', '515.125.4269', '2007-09-19', 'FI_ACCOUNT', 8000, NULL, 107, 100),
    (114, 'Den', 'Raphaely', 'DRAPHAEL', '515.127.4561', '2002-12-07', 'PU_MAN', 11000, NULL, 101, 30),
    (115, 'Alexander', 'Khoo', 'AKHOO', '515.127.4562', '2003-05-18', 'PU_CLERK', 3100, NULL, 114, 30),
    (116, 'Shelli', 'Baida', 'SBAIDA', '515.127.4563', '2005-12-24', 'PU_CLERK', 2900, NULL, 114, 30),
    (117, 'Sigal', 'Tobias', 'STOBIAS', '515.127.4564', '2005-07-24', 'PU_CLERK', 2800, NULL, 114, 30),
    (118, 'Guy', 'Himuro', 'GHIMURO', '515.127.4565', '2006-10-15', 'PU_CLERK', 2600, NULL, 114, 30),
    (119, 'Kevin', 'Mourgos', 'KMOURGOS', '515.127.4566', '2007-11-14', 'PU_CLERK', 2500, NULL, 114, 30),
    (121, 'Adam', 'Fripp', 'AFRIPP', '650.123.2234', '2005-04-10', 'SH_CLERK', 8200, NULL, 100, 50),
    (120, 'Matthew', 'Weiss', 'MWEISS', '650.123.1234', '2004-07-18', 'SH_CLERK', 8000, NULL, 121, 50),
    (145, 'John', 'Russell', 'JRUSSEL', '515.124.4567', '2004-10-01', 'SA_MAN', 14000, 0.4, 100, 80),
    (200, 'Jennifer', 'Whalen', 'JWHALEN', '515.123.4444', '2003-09-17', 'AD_ASST', 4400, NULL, 101, 10),
    (201, 'Michael', 'Hartstein', 'MHARTSTE', '515.123.5555', '2004-02-17', 'MK_MAN', 13000, NULL, 100, 20),
    (203, 'Susan', 'Mavris', 'SMAVRIS', '515.123.7777', '2002-06-07', 'HR_REP', 6500, NULL, 101, 40),
    (204, 'Hermann', 'Baer', 'HBAER', '515.123.8888', '2002-06-07', 'PR_REP', 10000, NULL, 101, 70),
    (205, 'Shelley', 'Higgins', 'SHIGGINS', '515.123.8080', '2002-06-07', 'AC_MGR', 12000, NULL, 101, 110);
    """
    cursor.execute(sql_insert_employees)
    conn.commit()
    print("Datos insertados en EMPLOYEES")

    # Actualizar la tabla DEPARTMENTS con los manager_id correctos
    sql_update_managers = """
    UPDATE departments
    SET manager_id = CASE department_id
        WHEN 10 THEN 200
        WHEN 20 THEN 201
        WHEN 30 THEN 114
        WHEN 40 THEN 203
        WHEN 50 THEN 121
        WHEN 60 THEN 103
        WHEN 70 THEN 204
        WHEN 80 THEN 145
        WHEN 90 THEN 100
        WHEN 100 THEN 108
        WHEN 110 THEN 205
    END
    WHERE department_id IN (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110);
    """
    cursor.execute(sql_update_managers)
    conn.commit()
    print("manager_id actualizado en la tabla DEPARTMENTS")

    # Insertar datos en JOB_HISTORY
    sql_insert_job_history = """
    INSERT OR IGNORE INTO job_history (employee_id, start_date, end_date, job_id, department_id) VALUES
    (102, '2001-01-13', '2006-07-24', 'IT_PROG', 60),
    (103, '2006-01-03', '2007-01-03', 'IT_PROG', 60),
    (104, '2007-05-21', '2008-01-01', 'IT_PROG', 60),
    (105, '2007-02-07', '2008-01-01', 'IT_PROG', 60),
    (106, '2006-02-05', '2008-01-01', 'IT_PROG', 60),
    (107, '2002-08-17', '2007-10-17', 'FI_MGR', 100),
    (108, '2002-08-16', '2007-10-16', 'FI_ACCOUNT', 100),
    (109, '2007-09-28', '2008-01-01', 'FI_ACCOUNT', 100),
    (110, '2005-09-30', '2008-01-01', 'FI_ACCOUNT', 100),
    (111, '2006-03-07', '2008-01-01', 'FI_ACCOUNT', 100),
    (112, '2007-12-07', '2008-01-01', 'FI_ACCOUNT', 100),
    (113, '2007-09-19', '2008-01-01', 'FI_ACCOUNT', 100);
    """
    cursor.execute(sql_insert_job_history)
    conn.commit()
    print("Datos insertados en JOB_HISTORY")

    # ------------------ RESUMEN FINAL ------------------
    print("\n=== RESUMEN DE LA BASE DE DATOS HR ===")
    print(f"Motor de BD usado: SQLite")
    print(f"Archivo de BD: hr_database.db")
    print(f"Tablas creadas y pobladas: {len(tablas)}")
    print("\nProceso de creación de base de datos finalizado.")

    conn.close()

if __name__ == "__main__":
    crear_base_de_datos()


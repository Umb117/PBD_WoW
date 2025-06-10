import os
import importlib.util
import psycopg2


def create_analytics_db():
    print(os.getenv('DB_PORT'))
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME') ,
        user=os.getenv('DB_USER') ,
        password=os.getenv('DB_PASSWORD') ,
        host=os.getenv('DB_HOST') ,
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()

    cur.execute("""DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'analytic') THEN
                CREATE ROLE analytic NOLOGIN;
                GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytic;
                ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytic;
            END IF;
        END $$;"""
    )

    analyst_names = os.getenv('ANALYST_NAMES' , '').split(',')
    for name in analyst_names:
        print(name)
        if not name.strip():
            continue

        username = name.strip().lower()
        password = f"{username}_123"

        cur.execute(f"""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{username}') THEN
                            CREATE USER {username} WITH PASSWORD '{password}';
                        END IF;
                    END
                    $$;
                """)

        cur.execute(f"GRANT analytic TO {username};")

    conn.commit()
    cur.close()
    conn.close()

def seed_all():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME") ,
        user=os.getenv("DB_USER") ,
        password=os.getenv("DB_PASSWORD") ,
        host=os.getenv("DB_HOST") ,
        port=os.getenv("DB_PORT")
    )

    try:
        seed_version = os.getenv("SEED_VERSION" , "all").lower()
        cur = conn.cursor()

        target_version = None
        if seed_version != "all":
            try:
                target_version = int(seed_version.lstrip('v'))
            except ValueError:
                print(f"Некорректный формат SEED_VERSION: {seed_version}")
                return

        for file in sorted(os.listdir("seeds")):
            if file.endswith(".py") and file != "__init__.py":
                version = file.split(".")[0]
                file_version = file.split('_')[0]
                try:
                    version_num = int(file_version.lstrip('v'))
                except ValueError:
                    print(f"Пропуск файла с некорректным именем: {file}")
                    continue

                if seed_version == "all":
                    execute = True
                elif target_version is not None:
                    execute = (version_num <= target_version)
                else:
                    execute = False

                if execute:
                    print(f"Seeding {version}...")
                    spec = importlib.util.spec_from_file_location(version ,f"seeds/{file}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    module.seed(cur)
                    conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        conn.close()
        print("Seeded all seeds")


if os.getenv('APP_ENV') == 'dev':
    seed_all()
    if not (os.getenv('ANALYST_NAMES') == "" or os.getenv('ANALYST_NAMES') is None):
        create_analytics_db()
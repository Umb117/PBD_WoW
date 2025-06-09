import os
import subprocess
import filecmp
import tempfile
import sys
import re

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "wow_db")
DB_USER = os.getenv("POSTGRES_USER", "migrator_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")

def collect_migration_pairs(migrations_path="./migrations"):
    files = os.listdir(migrations_path)
    up_migrations = {}
    down_migrations = {}

    for f in files:
        match = re.match(r'([VU])(\d+)__.+\.sql$', f)
        if match:
            kind, number = match.groups()
            if kind == 'V':
                up_migrations[number] = f
            elif kind == 'U':
                down_migrations[number] = f

    migration_numbers = sorted(set(up_migrations.keys()) & set(down_migrations.keys()), key=int)
    return [(up_migrations[num], down_migrations[num]) for num in migration_numbers]

MIGRATIONS = collect_migration_pairs()


def run_sql_file(filename):
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD
    print(f"Running SQL file: {filename}")

    subprocess.run([
        "psql",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-f", f"./migrations/{filename}"
    ], check=True, env=env)

def dump_schema(filename):
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    with open(filename, "w") as f:
        subprocess.run([
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", DB_NAME,
            "--schema-only",
            "--no-owner",
            "--no-privileges"
        ], check=True, env=env, stdout=f)

def clean_db():
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD
    subprocess.run([
        "psql",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-c", "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    ], check=True, env=env)
    print("Database cleaned.")

def main():
    clean_db()

    for idx, (up_file, down_file) in enumerate(MIGRATIONS, 1):
        print(f"\n=== Testing migration #{idx} ===")

        run_sql_file(up_file)
        tmp1 = tempfile.NamedTemporaryFile(delete=False)
        dump_schema(tmp1.name)
        tmp1.close()

        run_sql_file(down_file)

        run_sql_file(up_file)
        tmp2 = tempfile.NamedTemporaryFile(delete=False)
        dump_schema(tmp2.name)
        tmp2.close()

        if not filecmp.cmp(tmp1.name, tmp2.name, shallow=False):
            print(f"ERROR: Migration {up_file} is NOT idempotent — dumps differ!")
            print(f"First dump: {tmp1.name}")
            print(f"Second dump: {tmp2.name}")
            sys.exit(1)
        else:
            print(f"Migration {up_file} is idempotent.")

        clean_db()

        os.unlink(tmp1.name)
        os.unlink(tmp2.name)

    print("\nAll migrations passed idempotency test!")

if __name__ == "__main__":
    main()

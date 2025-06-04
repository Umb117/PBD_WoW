DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'migrator_user') THEN
    CREATE USER migrator_user WITH PASSWORD 'admin123';
    ALTER USER migrator_user CREATEDB CREATEROLE;
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_database
    WHERE datname = 'wow_db'
  ) THEN
    CREATE DATABASE wow_db WITH OWNER migrator_user;
END IF;
END $$;
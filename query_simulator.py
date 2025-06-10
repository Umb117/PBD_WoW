import os
import time
import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_sql_file(file_path):
    commands = []
    try:
        with open(file_path, 'r') as f:
            command = ""
            for line in f:
                line = line.strip()
                if line and not line.startswith('--'):
                    command += line + " "
                    if line.endswith(';'):
                        commands.append(command.strip())
                        command = ""
    except Exception as e:
        logger.error(f"Failed to load SQL file {file_path}: {e}")
    logger.info(f"Loaded {len(commands)} commands from {file_path}")
    return commands

def load_queries(file_path):
    queries = []
    try:
        with open(file_path , 'r') as f:
            query = ""
            for line in f:
                line = line.strip()
                if line and not line.startswith('--'):
                    query += line + " "
                    if line.endswith(';'):
                        queries.append(query.strip())
                        query = ""
    except Exception as e:
        logger.error(f"Failed to load queries: {e}")
    logger.info(f"Loaded {len(queries)} queries from {file_path}")
    return queries

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME") ,
        user=os.getenv("DB_USER") ,
        password=os.getenv("DB_PASSWORD") ,
        host=os.getenv("DB_HOST") ,
        port=os.getenv("DB_PORT")
    )

def apply_indexes(conn, indexes_file="/app/query_simulator/add_indexes.sql"):
    indexes = load_sql_file(indexes_file)
    if not indexes:
        logger.warning(f"No indexes to apply from {indexes_file}")
        return

    cursor = conn.cursor()
    try:
        for index in indexes:
            try:
                logger.info(f"Applying index: {index[:50]}...")
                cursor.execute(index)
                conn.commit()
                logger.info(f"Successfully applied index: {index[:50]}...")
            except Exception as e:
                logger.error(f"Failed to apply index: {e}")
                conn.rollback()
        logger.info("All indexes applied successfully")
    finally:
        cursor.close()

def run_queries():
    queries = load_queries("/app/query_simulator/queries.sql")
    if not queries:
        logger.error("No queries to execute. Exiting.")
        return

    conn = connect_db()
    apply_indexes(conn , "/app/query_simulator/add_indexes.sql")
    cursor = conn.cursor()
    for query in queries:
        logger.info(query[:50])

    try:
        while True:
            for query in queries:
                try:
                    tagged_query = f"/* app=query_simulator */ {query}"
                    cursor.execute(tagged_query)
                    conn.commit()
                    logger.info(f"Executed query: {tagged_query[:50]}...")
                except Exception as e:
                    logger.error(f"Query failed: {e}")
                    conn.rollback()
                time.sleep(float(os.getenv("QUERY_INTERVAL" , 1)))
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_queries()
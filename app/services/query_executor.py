import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def run_query(sql: str) -> tuple:
    conn = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            results = cur.fetchall()
            return list(results), None
    except Exception as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()

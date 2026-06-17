import re
import mariadb
from ai_tools.db import get_connection

_MAX_ROWS = 500
_SELECT_PATTERN = re.compile(r"^select\b", re.IGNORECASE)


def run_query(sql: str) -> list:
    sql = sql.strip()
    if not _SELECT_PATTERN.match(sql):
        raise ValueError("Only SELECT queries are allowed")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)

        if cur.description is None:
            return []

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchmany(_MAX_ROWS)
        return [dict(zip(columns, row)) for row in rows]
    except mariadb.Error as e:
        raise ValueError(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()

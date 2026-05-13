from ai_tools.db import get_connection


def get_latest_log(heatpump_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM heatpump_log
        WHERE heatpump_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """,
        (heatpump_id,),
    )

    row = cur.fetchone()

    if not row:
        return None

    columns = [desc[0] for desc in cur.description]
    result = dict(zip(columns, row))

    cur.close()
    conn.close()

    return result

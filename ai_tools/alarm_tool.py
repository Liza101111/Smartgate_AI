from ai_tools.db import get_connection


def get_recent_alarms(heatpump_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM alarms
        WHERE heatpump_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
    """,
        (heatpump_id,),
    )

    rows = cur.fetchall()

    if not rows:
        return []

    columns = [desc[0] for desc in cur.description]
    result = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    return result

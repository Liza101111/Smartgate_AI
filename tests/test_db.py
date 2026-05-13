# Run from project root:
# python tests/test_db.py

from ai_tools.db import get_connection

mar_con = get_connection()

cur = mar_con.cursor()

cur.execute("""
    SELECT heatpump_id, timestamp
    FROM heatpump_log
    ORDER BY timestamp DESC
    LIMIT 5
""")

for row in cur.fetchall():
    print(row)

cur.close()
mar_con.close()

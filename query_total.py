import sqlite3
conn = sqlite3.connect('kpi_history.db')
print(conn.execute("SELECT * FROM kpi_daily WHERE Ma_NV='TỔNG'").fetchall())
conn.close()

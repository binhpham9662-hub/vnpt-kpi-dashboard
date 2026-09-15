import sqlite3
conn = sqlite3.connect('kpi_history.db')
cursor = conn.cursor()
cursor.execute("SELECT Ma_NV, Ten_NV, To_KTDB FROM kpi_daily WHERE Ma_NV='TỔNG' LIMIT 1")
print(cursor.fetchone())
conn.close()

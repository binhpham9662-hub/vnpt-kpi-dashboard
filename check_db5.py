import sqlite3
conn = sqlite3.connect('kpi_history.db')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT Ngay_Bao_Cao FROM kpi_daily ORDER BY Ngay_Bao_Cao DESC LIMIT 5;")
print(cursor.fetchall())
conn.close()

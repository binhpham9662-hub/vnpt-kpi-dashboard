import sqlite3
conn = sqlite3.connect(r'H:\web-bao-cao\kpi_history.db')
c = conn.cursor()
c.execute("SELECT Ngay_Bao_Cao, COUNT(*) FROM kpi_daily GROUP BY Ngay_Bao_Cao ORDER BY Ngay_Bao_Cao DESC LIMIT 5")
print('--- kpi_daily ---')
for row in c.fetchall(): print(row)

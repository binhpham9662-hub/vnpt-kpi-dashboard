import sqlite3
conn = sqlite3.connect(r'H:\web-bao-cao\kpi_history.db')
c = conn.cursor()
c.execute("SELECT Ngay_Bao_Cao, COUNT(*) FROM pending_tickets WHERE Loai_Phieu='PTTB' GROUP BY Ngay_Bao_Cao")
for row in c.fetchall(): print(row)

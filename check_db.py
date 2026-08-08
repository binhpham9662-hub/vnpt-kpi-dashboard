import sqlite3
conn = sqlite3.connect('kpi_history.db')
c = conn.cursor()
c.execute("SELECT Ngay_Bao_Cao, COUNT(*) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' GROUP BY Ngay_Bao_Cao")
for row in c.fetchall():
    print(row)
c.execute("SELECT Ma_TB, Ngay_Bao_Cao FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ma_TB IN ('b0912300443', 'ctythanglonghni', 'bibo6868')")
for row in c.fetchall():
    print('Found missing:', row)
conn.close()

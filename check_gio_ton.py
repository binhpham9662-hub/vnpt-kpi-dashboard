import sqlite3
conn = sqlite3.connect('kpi_history.db')
c = conn.cursor()
c.execute("SELECT Ma_TB, Gio_Ton FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ma_TB IN ('b0912300443', 'ctythanglonghni', 'bibo6868')")
with open('debug_gio_ton.txt', 'w', encoding='utf-8') as f:
    for row in c.fetchall():
        f.write(repr(row) + '\n')
conn.close()

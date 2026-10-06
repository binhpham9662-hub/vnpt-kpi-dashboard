import sqlite3
conn = sqlite3.connect('kpi_history.db')
c = conn.cursor()
r = c.execute("SELECT sum(SM3), sum(SM4), sum(SM3_Tru), sum(SM4_Tru) FROM kpi_daily WHERE Ngay_Bao_Cao='2026-10-06' AND Ma_NV != 'TỔNG'").fetchone()
print(r)
# Fix the TOTAL row explicitly!
c.execute("UPDATE kpi_daily SET SM3=?, SM4=?, SM3_Tru=?, SM4_Tru=? WHERE Ngay_Bao_Cao='2026-10-06' AND Ma_NV='TỔNG'", r)
conn.commit()
conn.close()

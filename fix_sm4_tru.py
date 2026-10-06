import sqlite3
conn = sqlite3.connect('kpi_history.db')
conn.execute("UPDATE kpi_daily SET SM4_Tru = SM4 - HT_Dat WHERE Ngay_Bao_Cao='2026-10-06'")
conn.commit()
conn.close()

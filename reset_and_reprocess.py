import sqlite3
import database
conn = sqlite3.connect('kpi_history.db')
conn.execute("UPDATE kpi_daily SET SM3=0, SM4=0, SM3_Tru=0, SM4_Tru=0, HT_Dat=0, HT_Khong_Dat=0 WHERE Ngay_Bao_Cao='2026-10-06'")
conn.commit()
conn.close()

database.process_repeated_tickets_excel('downloads/SM1_C12_20261006_081554.xlsx', '2026-10-06')
database.process_sm4_excel('downloads/SM4_C11_20261006_151025.xlsx', '2026-10-06')

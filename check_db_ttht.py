import sqlite3
conn = sqlite3.connect('kpi_history.db')
cursor = conn.cursor()
cursor.execute("SELECT Ma_NV, SM4_Dat_HT, SM4_Khong_Dat_HT FROM kpi_daily WHERE Ngay_Bao_Cao='2026-09-15' AND (SM4_Dat_HT > 0 OR SM4_Khong_Dat_HT > 0)")
rows = cursor.fetchall()
for r in rows:
    print(r)
conn.close()

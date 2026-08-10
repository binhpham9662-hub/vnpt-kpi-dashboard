import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
query = """
SELECT Ma_TB as 'Mã Thuê Bao', MAX(Gio_Ton) as 'Giờ/Ngày Tồn', MAX(Ly_Do_Ton) as 'Lý Do Tồn'
FROM pending_tickets
WHERE Ngay_Bao_Cao = (SELECT MAX(Ngay_Bao_Cao) FROM pending_tickets WHERE Loai_Phieu = 'BRCD_LAP' AND Ngay_Bao_Cao <= ?) AND Loai_Phieu = 'BRCD_LAP' AND NVKT = ?
GROUP BY Ma_TB
ORDER BY MAX(Gio_Ton) DESC
"""
df = pd.read_sql_query(query, conn, params=['2026-08-10', 'VNPT016712-Nguyễn Hải Quân'])
print("Count for VNPT016712-Nguyễn Hải Quân:", len(df))
df2 = pd.read_sql_query(query, conn, params=['2026-08-10', 'Nguyễn Hải Quân'])
print("Count for Nguyễn Hải Quân:", len(df2))

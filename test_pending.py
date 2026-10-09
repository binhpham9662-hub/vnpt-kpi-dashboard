import sqlite3
import pandas as pd

conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT COUNT(*) FROM pending_tickets WHERE Ngay_Bao_Cao = '2026-10-07' AND Loai_Phieu = 'BRCD_KHONG_DAT'", conn)
print(df)

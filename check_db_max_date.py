import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT MAX(Ngay_Bao_Cao) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP'", conn)
print(df)
df = pd.read_sql_query("SELECT NVKT, COUNT(*) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-10' GROUP BY NVKT", conn)
print("Data for 2026-08-10:")
print(df)
df = pd.read_sql_query("SELECT NVKT, COUNT(*) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-09' GROUP BY NVKT", conn)
print("Data for 2026-08-09:")
print(df)

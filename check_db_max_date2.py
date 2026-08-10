import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT MAX(Ngay_Bao_Cao) as max_date FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP'", conn)
print(df)
df = pd.read_sql_query("SELECT NVKT, COUNT(*) as c FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-10' GROUP BY NVKT", conn)
df.to_csv('debug_db_max_10.txt', index=False)
df = pd.read_sql_query("SELECT NVKT, COUNT(*) as c FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-09' GROUP BY NVKT", conn)
df.to_csv('debug_db_max_09.txt', index=False)

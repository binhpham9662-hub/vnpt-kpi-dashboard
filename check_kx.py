import sqlite3
import pandas as pd
conn = sqlite3.connect('H:\\web-bao-cao\\kpi_history.db')
df = pd.read_sql_query("SELECT * FROM pending_tickets WHERE NVKT='Không xác định' AND Ngay_Bao_Cao='2026-08-11'", conn)
df.to_csv('H:\\web-bao-cao\\debug_kx.csv', index=False)
print(f"Found {len(df)} rows")

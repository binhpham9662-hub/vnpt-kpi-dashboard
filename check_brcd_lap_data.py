import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT DISTINCT NVKT, To_KTDB FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' LIMIT 20", conn)
print(df)

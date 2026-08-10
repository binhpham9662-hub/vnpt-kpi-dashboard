import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT Ngay_Bao_Cao, NVKT FROM pending_tickets WHERE Ma_TB='01653329239' AND Loai_Phieu='BRCD_LAP' ORDER BY Ngay_Bao_Cao DESC", conn)
print(df)

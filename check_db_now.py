import sqlite3
import pandas as pd
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
conn = sqlite3.connect('H:\\web-bao-cao\\kpi_history.db')
df = pd.read_sql_query("SELECT NVKT, COUNT(*) as cnt FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-11' GROUP BY NVKT", conn)
print(df)

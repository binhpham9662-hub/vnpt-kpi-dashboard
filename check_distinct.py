import sqlite3
import pandas as pd
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

conn = sqlite3.connect('H:\\web-bao-cao\\kpi_history.db')

df_count = pd.read_sql_query("SELECT COUNT(*) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-12'", conn)
print("Total rows:", df_count.iloc[0,0])

df_dist = pd.read_sql_query("SELECT COUNT(DISTINCT Ma_TB) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-12'", conn)
print("Distinct Ma_TB:", df_dist.iloc[0,0])

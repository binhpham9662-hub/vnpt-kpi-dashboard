import sqlite3
import pandas as pd
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
conn = sqlite3.connect('H:\\web-bao-cao\\kpi_history.db')
df = pd.read_sql_query("SELECT COUNT(*) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-12'", conn)
print("Tickets on 2026-08-12:", df.iloc[0,0])

df2 = pd.read_sql_query("SELECT COUNT(*) FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP' AND Ngay_Bao_Cao='2026-08-11'", conn)
print("Tickets on 2026-08-11:", df2.iloc[0,0])

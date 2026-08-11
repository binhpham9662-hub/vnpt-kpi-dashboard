import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.path.append('H:\\web-bao-cao')
from database import process_repeated_tickets_excel
import pandas as pd
import sqlite3

# run process
process_repeated_tickets_excel("H:\\web-bao-cao\\downloads\\SM1_C12_20260811_081557.xlsx", "2026-08-11")

# check db
conn = sqlite3.connect('H:\\web-bao-cao\\kpi_history.db')
df = pd.read_sql_query("SELECT NVKT, COUNT(*) as cnt FROM pending_tickets WHERE Ngay_Bao_Cao='2026-08-11' AND Loai_Phieu='BRCD_LAP' GROUP BY NVKT", conn)
print(df)

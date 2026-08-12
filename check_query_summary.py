import sqlite3
import pandas as pd
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

conn = sqlite3.connect('H:\\web-bao-cao\\kpi_history.db')

query = """
SELECT To_KTDB, NVKT, COUNT(DISTINCT Ma_TB) as Total_Tickets
FROM pending_tickets
WHERE Ngay_Bao_Cao = '2026-08-12' AND Loai_Phieu = 'BRCD_LAP'
GROUP BY To_KTDB, NVKT
ORDER BY To_KTDB ASC, Total_Tickets DESC
"""
df = pd.read_sql_query(query, conn)
print(df)
print("Sum Total_Tickets:", df['Total_Tickets'].sum())

import sqlite3
import pandas as pd

conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT * FROM kpi_daily WHERE Ten_NV LIKE '%Thọ%' AND Ngay_Bao_Cao = '2026-10-06'", conn)
df.to_csv('test_db_tho.csv', index=False, encoding='utf-8-sig')
conn.close()

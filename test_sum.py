import sqlite3
import pandas as pd

conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT To_KTDB, SUM(SM3) as sum_sm3, SUM(SM4) as sum_sm4 FROM kpi_daily WHERE Ngay_Bao_Cao = '2026-10-07' GROUP BY To_KTDB", conn)
df.to_csv('test_sum.csv', index=False, encoding='utf-8-sig')
df2 = pd.read_sql_query("SELECT Ten_NV, To_KTDB, SM3, SM4 FROM kpi_daily WHERE Ngay_Bao_Cao = '2026-10-07' AND Ten_NV LIKE '%Thọ%'", conn)
df2.to_csv('test_tho.csv', index=False, encoding='utf-8-sig')

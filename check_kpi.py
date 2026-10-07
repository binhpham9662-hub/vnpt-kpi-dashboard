import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT * FROM kpi_daily WHERE Ngay_Bao_Cao = '2026-10-07'", conn)
df.to_csv('kpi_20261007.csv', index=False, encoding='utf-8-sig')
print("SUM Tổ:", df[df['Ma_NV'] != 'TỔNG']['SM4'].sum())
print("SUM TỔNG:", df[df['Ma_NV'] == 'TỔNG']['SM4'].sum())

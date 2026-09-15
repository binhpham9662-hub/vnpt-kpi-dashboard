import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
df = pd.read_sql_query("SELECT * FROM kpi_daily WHERE Ngay_Bao_Cao = '2026-09-14';", conn)
conn.close()
df['To_KTDB'] = df['To_KTDB'].replace('Không xác định', 'Trung tâm Viễn thông Đông Anh')
print(df.groupby('To_KTDB')[['SM3', 'SM4']].sum())

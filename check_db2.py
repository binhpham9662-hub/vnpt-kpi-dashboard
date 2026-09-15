import sqlite3
import pandas as pd

conn = sqlite3.connect('kpi_history.db')
cursor = conn.cursor()

# Get the schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='kpi_daily';")
print('Schema:', cursor.fetchone()[0])

# Get yesterday's data
df = pd.read_sql_query("SELECT * FROM kpi_daily WHERE Ngay_Bao_Cao = '2026-09-14' LIMIT 10;", conn)
print('\nData:\n', df.to_string())

conn.close()

import sqlite3

conn = sqlite3.connect('kpi_history.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE kpi_daily ADD COLUMN SM3_Tru REAL;")
except Exception as e:
    print(e)
    
try:
    cursor.execute("ALTER TABLE kpi_daily ADD COLUMN SM4_Tru REAL;")
except Exception as e:
    print(e)
    
try:
    cursor.execute("ALTER TABLE kpi_daily ADD COLUMN HT_Dat REAL;")
except Exception as e:
    print(e)

try:
    cursor.execute("ALTER TABLE kpi_daily ADD COLUMN HT_Khong_Dat REAL;")
except Exception as e:
    print(e)
    
conn.commit()
conn.close()

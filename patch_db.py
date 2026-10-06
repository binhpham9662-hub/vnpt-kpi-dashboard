import sqlite3
import os

DB_PATH = 'kpi_history.db'

def patch_database():
    if not os.path.exists(DB_PATH):
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check existing columns in kpi_daily
    cursor.execute("PRAGMA table_info(kpi_daily)")
    columns = [row[1] for row in cursor.fetchall()]
    
    new_columns = ['SM3_Tru', 'SM4_Tru', 'HT_Dat', 'HT_Khong_Dat']
    for col in new_columns:
        if col not in columns:
            try:
                cursor.execute(f"ALTER TABLE kpi_daily ADD COLUMN {col} REAL DEFAULT 0")
                print(f"Added column {col} to kpi_daily")
            except Exception as e:
                print(f"Failed to add {col}: {e}")
                
    conn.commit()
    conn.close()

if __name__ == "__main__":
    patch_database()

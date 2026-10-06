import sqlite3

def fix_total_row():
    conn = sqlite3.connect('kpi_history.db')
    c = conn.cursor()
    
    # Get the latest date
    c.execute("SELECT max(Ngay_Bao_Cao) FROM kpi_daily")
    latest_date = c.fetchone()[0]
    
    if not latest_date:
        print("No data in DB")
        return
        
    print(f"Fixing TOTAL row for {latest_date}")
    
    # Sum up everything excluding the TOTAL row and excluding Không xác định (wait, actually Không xác định is mapped in app, in db it's still individual NV)
    c.execute('''
        SELECT sum(SM3_Tru), sum(SM4_Tru), sum(HT_Dat), sum(HT_Khong_Dat) 
        FROM kpi_daily 
        WHERE Ma_NV != 'TỔNG' AND Ngay_Bao_Cao = ?
    ''', (latest_date,))
    
    sums = c.fetchone()
    print('Calculated sums:', sums)
    
    if sums and sums[0] is not None:
        c.execute('''
            UPDATE kpi_daily 
            SET SM3_Tru=?, SM4_Tru=?, HT_Dat=?, HT_Khong_Dat=? 
            WHERE Ma_NV='TỔNG' AND Ngay_Bao_Cao = ?
        ''', (*sums, latest_date))
        
        print("Updated successfully")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_total_row()

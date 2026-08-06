import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

DB_PATH = 'kpi_history.db'
ZALO_PATH = 'zalo.xlsx'

def get_cycle_month(date_str):
    """
    Returns the cycle month. Cycle is from 26th of previous month to 25th of current month.
    E.g. 2026-06-25 -> 2026-06
         2026-06-26 -> 2026-07
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    if dt.day >= 26:
        if dt.month == 12:
            return f"{dt.year + 1}-01"
        else:
            return f"{dt.year}-{dt.month + 1:02d}"
    else:
        return dt.strftime('%Y-%m')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kpi_daily (
            Ngay_Bao_Cao TEXT,
            Ma_NV TEXT,
            Ten_NV TEXT,
            To_KTDB TEXT,
            Thang_Du_Lieu TEXT,
            SM1 REAL,
            SM2 REAL,
            SM3 REAL,
            SM4 REAL,
            SM5 REAL,
            SM6 REAL,
            PRIMARY KEY (Ngay_Bao_Cao, Ma_NV)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_tickets (
            Ngay_Bao_Cao TEXT,
            Loai_Phieu TEXT,
            Ma_TB TEXT,
            NVKT TEXT,
            To_KTDB TEXT,
            Gio_Ton TEXT,
            Ly_Do_Ton TEXT,
            PRIMARY KEY (Ngay_Bao_Cao, Loai_Phieu, Ma_TB)
        )
    ''')
    conn.commit()
    conn.close()

def clean_column_name(col):
    return str(col).strip().lower()

def process_and_insert_excel(excel_path, report_date=None, report_type="C1.1"):
    if report_date is None:
        report_date = datetime.now().strftime('%Y-%m-%d')
        
    try:
        # Load the report excel
        df = pd.read_excel(excel_path)
        
        # Sometimes header is not on the first row, find it
        header_row_idx = None
        for i, row in df.iterrows():
            row_str = " ".join([str(v).lower() for v in row.values])
            if 'mã nhân viên' in row_str or 'mã nv' in row_str or 'đơn vị' in row_str or 'sm1' in row_str:
                header_row_idx = i
                break
                
        if header_row_idx is not None:
            df = pd.read_excel(excel_path, header=header_row_idx+1)
            
        # Rename columns to standard names
        col_mapping = {}
        for col in df.columns:
            cl = clean_column_name(col)
            if ('mã nhân viên' in cl or 'mã nv' in cl or 'đơn vị' in cl) and 'Ma_NV' not in col_mapping.values(): 
                col_mapping[col] = 'Ma_NV'
            elif ('tên nhân viên' in cl or 'tên nv' in cl) and 'Ten_NV' not in col_mapping.values(): 
                col_mapping[col] = 'Ten_NV'
            elif 'sm1' in cl and 'SM1' not in col_mapping.values(): 
                col_mapping[col] = 'SM1'
            elif 'sm2' in cl and 'SM2' not in col_mapping.values(): 
                col_mapping[col] = 'SM2'
            elif 'sm3' in cl and 'SM3' not in col_mapping.values(): 
                col_mapping[col] = 'SM3'
            elif 'sm4' in cl and 'SM4' not in col_mapping.values(): 
                col_mapping[col] = 'SM4'
            elif 'tháng' in cl and 'Thang_Du_Lieu' not in col_mapping.values(): 
                col_mapping[col] = 'Thang_Du_Lieu'
            
        df = df.rename(columns=col_mapping)
        
        # Extract Ten_NV from Ma_NV if it's concatenated (e.g. VNPT016586-35.0106-tantv.hni-Trần Văn Tân)
        if 'Ma_NV' in df.columns:
            def extract_ma(val):
                parts = str(val).split('-')
                return parts[0].strip() if len(parts) > 0 else str(val)
            def extract_ten(val):
                parts = str(val).split('-')
                return parts[-1].strip() if len(parts) > 1 else ''
                
            if 'Ten_NV' not in df.columns:
                df['Ten_NV'] = df['Ma_NV'].apply(extract_ten)
            
            df['Ma_NV'] = df['Ma_NV'].apply(extract_ma)
        
        # Ensure we have the required columns
        required = ['Ma_NV', 'Ten_NV', 'SM1', 'SM2', 'SM3', 'SM4']
        for r in required:
            if r not in df.columns:
                df[r] = 0 if r.startswith('SM') else ''
                
        # Fill NA for numbers
        for col in ['SM1', 'SM2', 'SM3', 'SM4']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        # Load Zalo mapping
        mapping = {}
        if os.path.exists(ZALO_PATH):
            zalo_df = pd.read_excel(ZALO_PATH)
            if 'MA_NV' in zalo_df.columns and 'Tổ' in zalo_df.columns:
                def clean_zalo_ma(val):
                    return str(val).split('-')[0].strip().upper()
                zalo_df['MA_NV'] = zalo_df['MA_NV'].apply(clean_zalo_ma)
                # Clean team name
                zalo_df['Tổ'] = zalo_df['Tổ'].fillna('Không xác định').astype(str)
                mapping = dict(zip(zalo_df['MA_NV'], zalo_df['Tổ']))
        
        df['Ma_NV'] = df['Ma_NV'].astype(str).str.strip().str.upper()
        df['To_KTDB'] = df['Ma_NV'].map(mapping).fillna('Không xác định')
        df['Ngay_Bao_Cao'] = report_date
        
        if 'Thang_Du_Lieu' not in df.columns:
            df['Thang_Du_Lieu'] = get_cycle_month(report_date)
            
        records = df.to_dict('records')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for r in records:
            if not r.get('Ma_NV') or r.get('Ma_NV') == 'NAN': continue
            
            if report_type == "C1.2":
                # Lấy SM1 và SM2 từ file Excel của C1.2, lưu vào SM5 và SM6
                sm5 = r.get('SM1', 0)
                sm6 = r.get('SM2', 0)
                
                cursor.execute('''
                    INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM5, SM6)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                    Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                    SM5=excluded.SM5, SM6=excluded.SM6
                ''', (r['Ngay_Bao_Cao'], r['Ma_NV'], r['Ten_NV'], r['To_KTDB'], r['Thang_Du_Lieu'], sm5, sm6))
            else:
                sm1 = r.get('SM1', 0)
                sm2 = r.get('SM2', 0)
                sm3 = r.get('SM3', 0)
                sm4 = r.get('SM4', 0)
                
                cursor.execute('''
                    INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM1, SM2, SM3, SM4)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                    Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                    SM1=excluded.SM1, SM2=excluded.SM2, SM3=excluded.SM3, SM4=excluded.SM4
                ''', (r['Ngay_Bao_Cao'], r['Ma_NV'], r['Ten_NV'], r['To_KTDB'], r['Thang_Du_Lieu'], sm1, sm2, sm3, sm4))
            
        conn.commit()
        
        # Auto-patching missing days (up to 5 days back)
        dt_report = datetime.strptime(report_date, '%Y-%m-%d')
        for days_back in range(1, 6):
            prev_date = (dt_report - timedelta(days=days_back)).strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM kpi_daily WHERE Ngay_Bao_Cao = ? AND (SM1 IS NOT NULL OR SM5 IS NOT NULL)', (prev_date,))
            count = cursor.fetchone()[0]
            if count == 0:
                prev_thang = get_cycle_month(prev_date)
                for r in records:
                    if not r.get('Ma_NV') or r.get('Ma_NV') == 'NAN': continue
                    if report_type == "C1.2":
                        sm5 = r.get('SM1', 0)
                        sm6 = r.get('SM2', 0)
                        cursor.execute('''
                            INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM5, SM6)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                            Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                            SM5=excluded.SM5, SM6=excluded.SM6
                        ''', (prev_date, r['Ma_NV'], r['Ten_NV'], r['To_KTDB'], prev_thang, sm5, sm6))
                    else:
                        sm1 = r.get('SM1', 0)
                        sm2 = r.get('SM2', 0)
                        sm3 = r.get('SM3', 0)
                        sm4 = r.get('SM4', 0)
                        cursor.execute('''
                            INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM1, SM2, SM3, SM4)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                            Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                            SM1=excluded.SM1, SM2=excluded.SM2, SM3=excluded.SM3, SM4=excluded.SM4
                        ''', (prev_date, r['Ma_NV'], r['Ten_NV'], r['To_KTDB'], prev_thang, sm1, sm2, sm3, sm4))
                conn.commit()
                logging.info(f"Auto-patched missing data for {prev_date} using data from {report_date}")
            else:
                break
        
        conn.close()
        logging.info(f"Inserted {len(records)} records for date {report_date}")
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error(f"Error processing excel: {e}")
        return False

def get_kpi_for_date(target_date_str):
    """
    Returns KPI data for the given date, along with the 'yesterday' data for delta calculation.
    """
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
    yesterday_str = (target_date - timedelta(days=1)).strftime('%Y-%m-%d')
    day2_str = (target_date - timedelta(days=2)).strftime('%Y-%m-%d')
    day3_str = (target_date - timedelta(days=3)).strftime('%Y-%m-%d')
    day7_str = (target_date - timedelta(days=7)).strftime('%Y-%m-%d')
    
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        t.Ma_NV, t.Ten_NV, t.To_KTDB,
        t.SM1, t.SM2, t.SM3, t.SM4, t.SM5, t.SM6,
        y.SM1 as Y_SM1, y.SM2 as Y_SM2, y.SM3 as Y_SM3, y.SM4 as Y_SM4, y.SM5 as Y_SM5, y.SM6 as Y_SM6,
        d2.SM1 as D2_SM1, d2.SM2 as D2_SM2, d2.SM3 as D2_SM3, d2.SM4 as D2_SM4, d2.SM5 as D2_SM5, d2.SM6 as D2_SM6,
        d3.SM1 as D3_SM1, d3.SM2 as D3_SM2, d3.SM3 as D3_SM3, d3.SM4 as D3_SM4, d3.SM5 as D3_SM5, d3.SM6 as D3_SM6,
        d7.SM1 as D7_SM1, d7.SM2 as D7_SM2, d7.SM3 as D7_SM3, d7.SM4 as D7_SM4, d7.SM5 as D7_SM5, d7.SM6 as D7_SM6
    FROM kpi_daily t
    LEFT JOIN kpi_daily y ON t.Ma_NV = y.Ma_NV AND y.Ngay_Bao_Cao = ?
    LEFT JOIN kpi_daily d2 ON t.Ma_NV = d2.Ma_NV AND d2.Ngay_Bao_Cao = ?
    LEFT JOIN kpi_daily d3 ON t.Ma_NV = d3.Ma_NV AND d3.Ngay_Bao_Cao = ?
    LEFT JOIN kpi_daily d7 ON t.Ma_NV = d7.Ma_NV AND d7.Ngay_Bao_Cao = ?
    WHERE t.Ngay_Bao_Cao = ?
    """
    df = pd.read_sql_query(query, conn, params=(yesterday_str, day2_str, day3_str, day7_str, target_date_str))
    conn.close()
    
    # Fill NA for SM columns to avoid NoneType errors
    for col in ['SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'SM6']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calculate deltas for BRCĐ (SM3/SM4)
    df['Phieu_Khong_Dat_BRCD'] = df['SM4'] - df['SM3']
    df['Tang_Khong_Dat_BRCD'] = df['Phieu_Khong_Dat_BRCD'] - (df['Y_SM4'].fillna(0) - df['Y_SM3'].fillna(0))
    df['Tang_Khong_Dat_BRCD_2d'] = df['Phieu_Khong_Dat_BRCD'] - (df['D2_SM4'].fillna(0) - df['D2_SM3'].fillna(0))
    df['Tang_Khong_Dat_BRCD_3d'] = df['Phieu_Khong_Dat_BRCD'] - (df['D3_SM4'].fillna(0) - df['D3_SM3'].fillna(0))
    df['Tang_Khong_Dat_BRCD_7d'] = df['Phieu_Khong_Dat_BRCD'] - (df['D7_SM4'].fillna(0) - df['D7_SM3'].fillna(0))
    
    # Calculate deltas for CLCĐ (SM1/SM2)
    df['Phieu_Khong_Dat_CLCD'] = df['SM2'] - df['SM1']
    df['Tang_Khong_Dat_CLCD'] = df['Phieu_Khong_Dat_CLCD'] - (df['Y_SM2'].fillna(0) - df['Y_SM1'].fillna(0))
    df['Tang_Khong_Dat_CLCD_2d'] = df['Phieu_Khong_Dat_CLCD'] - (df['D2_SM2'].fillna(0) - df['D2_SM1'].fillna(0))
    df['Tang_Khong_Dat_CLCD_3d'] = df['Phieu_Khong_Dat_CLCD'] - (df['D3_SM2'].fillna(0) - df['D3_SM1'].fillna(0))
    df['Tang_Khong_Dat_CLCD_7d'] = df['Phieu_Khong_Dat_CLCD'] - (df['D7_SM2'].fillna(0) - df['D7_SM1'].fillna(0))
    
    # Calculate deltas for BRCĐ Lặp (SM5/SM6)
    df['Tang_Khong_Dat_BRCD_Lap'] = df['SM5'] - df['Y_SM5'].fillna(0)
    df['Tang_Khong_Dat_BRCD_Lap_2d'] = df['SM5'] - df['D2_SM5'].fillna(0)
    df['Tang_Khong_Dat_BRCD_Lap_3d'] = df['SM5'] - df['D3_SM5'].fillna(0)
    df['Tang_Khong_Dat_BRCD_Lap_7d'] = df['SM5'] - df['D7_SM5'].fillna(0)
    
    # Keep old Phieu_Tang_Len for compatibility if needed elsewhere
    df['Phieu_Tang_Len'] = df['Tang_Khong_Dat_BRCD']
    
    # Ratios
    df['Ty_Le_CLCD'] = df.apply(lambda row: (row['SM1']/row['SM2']) if row['SM2'] > 0 else 0, axis=1)
    df['Ty_Le_BRCD'] = df.apply(lambda row: (row['SM3']/row['SM4']) if row['SM4'] > 0 else 0, axis=1)
    df['Ty_Le_BRCD_Lap'] = df.apply(lambda row: (row['SM5']/row['SM6']) if row['SM6'] > 0 else 0, axis=1)
    
    return df

def get_historical_kpi(start_date_str, end_date_str):
    """
    Fetches KPI records between start_date_str and end_date_str (inclusive).
    Used for analytics and charts.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, SM1, SM2, SM3, SM4, SM5, SM6
    FROM kpi_daily
    WHERE Ngay_Bao_Cao >= ? AND Ngay_Bao_Cao <= ?
    ORDER BY Ngay_Bao_Cao ASC
    """
    df = pd.read_sql_query(query, conn, params=(start_date_str, end_date_str))
    conn.close()
    return df

def save_pending_tickets(date_str, loai_phieu, tickets_dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Xóa dữ liệu cũ của ngày và loại phiếu này (để ghi đè)
    cursor.execute("DELETE FROM pending_tickets WHERE Ngay_Bao_Cao = ? AND Loai_Phieu = ?", (date_str, loai_phieu))
    
    for ma_tb, info in tickets_dict.items():
        nvkt = info.get("NVKT", "")
        to_ktdb = info.get("Tổ", "")
        gio_ton = info.get("GIO_TON", "")
        ly_do = info.get("LY_DO_TON", "")
        cursor.execute('''
            INSERT INTO pending_tickets (Ngay_Bao_Cao, Loai_Phieu, Ma_TB, NVKT, To_KTDB, Gio_Ton, Ly_Do_Ton)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date_str, loai_phieu, str(ma_tb), str(nvkt), str(to_ktdb), str(gio_ton), str(ly_do)))
    
    conn.commit()
    conn.close()

def get_pending_summary(date_str, loai_phieu):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT To_KTDB, NVKT, COUNT(Ma_TB) as Total_Tickets
    FROM pending_tickets
    WHERE Ngay_Bao_Cao = ? AND Loai_Phieu = ?
    GROUP BY To_KTDB, NVKT
    ORDER BY To_KTDB ASC, Total_Tickets DESC
    """
    df = pd.read_sql_query(query, conn, params=(date_str, loai_phieu))
    conn.close()
    return df

def get_pending_details(date_str, loai_phieu, nvkt):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT Ma_TB as 'Mã Thuê Bao', Gio_Ton as 'Giờ/Ngày Tồn', Ly_Do_Ton as 'Lý Do Tồn'
    FROM pending_tickets
    WHERE Ngay_Bao_Cao = ? AND Loai_Phieu = ? AND NVKT = ?
    ORDER BY Gio_Ton DESC
    """
    df = pd.read_sql_query(query, conn, params=(date_str, loai_phieu, nvkt))
    conn.close()
    return df

if __name__ == '__main__':
    init_db()
    print("Database initialized.")

import re
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

ttht_logic = '''
def process_ttht_excel(file_path, date_str):
    import pandas as pd
    import glob
    import os
    import sqlite3
    import logging
    
    try:
        df_ttht = pd.read_excel(file_path)
        if 'Báo Hỏng ID' in df_ttht.columns:
            df_ttht = df_ttht.rename(columns={'Báo Hỏng ID': 'BAOHONG_ID'})
            
        # Find latest SM4 file
        sm4_files = glob.glob(os.path.join('downloads', 'SM4_C11_*.xlsx'))
        if not sm4_files:
            logging.error("Không tìm thấy file SM4 nào để đối soát.")
            return
            
        latest_sm4_path = max(sm4_files, key=os.path.getctime)
        df_sm4 = pd.read_excel(latest_sm4_path)
        
        # Merge
        df_merged = pd.merge(df_sm4, df_ttht[['BAOHONG_ID', 'Trễ chuyển hạ tầng']], on='BAOHONG_ID', how='inner')
        
        # Load Zalo mapping once
        zalo_account_map = {}
        try:
            ZALO_PATH = r"H:\\web-bao-cao\\zalo.xlsx"
            if os.path.exists(ZALO_PATH):
                zalo_df = pd.read_excel(ZALO_PATH)
                if 'Account' in zalo_df.columns and 'MA_NV' in zalo_df.columns:
                    zalo_df['Account'] = zalo_df['Account'].astype(str).str.strip().str.upper()
                    zalo_account_map = dict(zip(zalo_df['Account'], zalo_df['MA_NV']))
        except Exception as e:
            logging.error(f"Lỗi đọc zalo.xlsx: {e}")
            
        nvkt_mapping = {}
        total_file_dat_ht = 0
        total_file_khong_dat_ht = 0
        
        for idx, row in df_merged.iterrows():
            # NVKT logic exactly as in SM4
            nvkt = "Không xác định"
            nguoi_khoa = str(row.get('NGUOI_KHOA', ''))
            if nguoi_khoa and nguoi_khoa.lower() != 'nan':
                nguoi_khoa = nguoi_khoa.strip(' ,')
                parts = nguoi_khoa.split('-')
                if len(parts) >= 3:
                    ma_nv = parts[0].strip()
                    ten_nv = parts[-1].strip()
                    nvkt = f"{ma_nv}-{ten_nv}"
                elif len(parts) == 2:
                    ma_nv = parts[0].strip()
                    ten_nv = parts[-1].strip()
                    nvkt = f"{ma_nv}-{ten_nv}"
                else:
                    nvkt = nguoi_khoa
            
            if nvkt == "Không xác định" or nvkt == "":
                ten_kv = str(row.get('TEN_KV', ''))
                if ten_kv and '(' in ten_kv:
                    prefix = ten_kv.split('(')[0]
                    parts = prefix.split('-')
                    if len(parts) > 0:
                        account = parts[-1].strip().upper()
                        if account in zalo_account_map:
                            nvkt = str(zalo_account_map[account])
                        else:
                            nvkt = account
            
            if nvkt == "Không xác định" or nvkt == "":
                nvkt = str(row.get('TEN_NV', 'Không xác định'))
                if 'NGUOI_XU_LY' in row: nvkt = str(row['NGUOI_XU_LY'])
                
            ma_nv_extracted = nvkt.split('-')[0].strip() if '-' in nvkt else nvkt
            
            tre_ht = str(row.get('Trễ chuyển hạ tầng', '')).strip().upper()
            dat_ht = 0
            khong_dat_ht = 0
            if tre_ht == 'DAT' or tre_ht == 'ĐẠT':
                dat_ht = 1
                total_file_dat_ht += 1
            elif tre_ht == 'KHONG DAT' or tre_ht == 'KHÔNG ĐẠT':
                khong_dat_ht = 1
                total_file_khong_dat_ht += 1
                
            if ma_nv_extracted not in nvkt_mapping:
                nvkt_mapping[ma_nv_extracted] = {'dat_ht': 0, 'khong_dat_ht': 0}
            nvkt_mapping[ma_nv_extracted]['dat_ht'] += dat_ht
            nvkt_mapping[ma_nv_extracted]['khong_dat_ht'] += khong_dat_ht

        DB_PATH = 'kpi_history.db'
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for ma_nv_extracted, data in nvkt_mapping.items():
            if ma_nv_extracted == "Không xác định" or not ma_nv_extracted: continue
            cursor.execute("""
                UPDATE kpi_daily SET SM4_Dat_HT=?, SM4_Khong_Dat_HT=? 
                WHERE Ngay_Bao_Cao=? AND Ma_NV=?
            """, (data['dat_ht'], data['khong_dat_ht'], date_str, ma_nv_extracted))
            
        cursor.execute("""
            UPDATE kpi_daily SET SM4_Dat_HT=?, SM4_Khong_Dat_HT=? 
            WHERE Ngay_Bao_Cao=? AND Ma_NV='TỔNG'
        """, (total_file_dat_ht, total_file_khong_dat_ht, date_str))
            
        conn.commit()
        conn.close()
        
        logging.info(f"Đã xử lý file TTHT, cập nhật giảm trừ HT cho {len(nvkt_mapping)} NVKT (Đạt HT: {total_file_dat_ht}, Không Đạt HT: {total_file_khong_dat_ht}) cho ngày {date_str}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error(f"Lỗi khi xử lý file TTHT Excel: {e}")
'''

start_idx = content.find('def process_ttht_excel')
if start_idx != -1:
    new_content = content[:start_idx] + ttht_logic
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Patched database.py successfully.')
else:
    print('Could not find process_ttht_excel')

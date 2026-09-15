import os

file_path = r'H:\web-bao-cao\database.py'

func = '''
def process_sm4_excel(file_path, date_str):
    try:
        df = pd.read_excel(file_path)
        
        # Load Zalo mapping once
        zalo_account_map = {}
        try:
            import os
            ZALO_PATH = r"H:\\web-bao-cao\\zalo.xlsx"
            if os.path.exists(ZALO_PATH):
                zalo_df = pd.read_excel(ZALO_PATH)
                if 'Account' in zalo_df.columns and 'MA_NV' in zalo_df.columns:
                    zalo_df['Account'] = zalo_df['Account'].astype(str).str.strip().str.upper()
                    zalo_account_map = dict(zip(zalo_df['Account'], zalo_df['MA_NV']))
        except Exception as e:
            logging.error(f"Lỗi đọc zalo.xlsx: {e}")
            
        nvkt_mapping = {}
        tickets = {}
        
        for idx, row in df.iterrows():
            ma_tb = str(row.get('MA_TB', ''))
            to_ktdb = str(row.get('TEN_DOI', 'Không xác định'))
            ngay_bao_hong = str(row.get('NGAY_BAO_HONG', ''))
            nguyen_nhan = str(row.get('NGUYEN_NHAN', ''))
            
            # NVKT logic
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
            
            # Extract NVKT from TEN_KV if NGUOI_KHOA is empty
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
            
            # Fallback
            if nvkt == "Không xác định" or nvkt == "":
                nvkt = str(row.get('TEN_NV', 'Không xác định'))
                if 'NGUOI_XU_LY' in row: nvkt = str(row['NGUOI_XU_LY'])
                
            ma_nv_extracted = nvkt.split('-')[0].strip() if '-' in nvkt else nvkt
            ten_nv_extracted = nvkt.split('-')[1].strip() if '-' in nvkt else ''
                
            dat_ko_hen = row.get('DAT_KO_HEN', 0)
            
            if ma_nv_extracted not in nvkt_mapping:
                nvkt_mapping[ma_nv_extracted] = {'ten': ten_nv_extracted, 'to': to_ktdb, 'sm3': 0, 'sm4': 0}
                
            nvkt_mapping[ma_nv_extracted]['sm4'] += 1
            if dat_ko_hen == 1:
                nvkt_mapping[ma_nv_extracted]['sm3'] += 1
            else:
                # Add to failed tickets
                gio_ton = f"Báo hỏng: {ngay_bao_hong}"
                tickets[f"{ma_tb}_{idx}"] = {
                    "Tổ": to_ktdb,
                    "NVKT": nvkt,
                    "GIO_TON": gio_ton,
                    "LY_DO_TON": nguyen_nhan
                }
                
        # Ghi vao kpi_daily
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        thang_du_lieu = get_cycle_month(date_str)
        
        for ma_nv_extracted, data in nvkt_mapping.items():
            if ma_nv_extracted == "Không xác định" or not ma_nv_extracted: continue
            sm3 = data['sm3']
            sm4 = data['sm4']
            ten_nv_extracted = data['ten']
            to_ktdb = data['to']
            cursor.execute(\'\'\'
                INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM3, SM4)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                SM3=excluded.SM3, SM4=excluded.SM4
            \'\'\', (date_str, ma_nv_extracted, ten_nv_extracted, to_ktdb, thang_du_lieu, sm3, sm4))
            
        conn.commit()
        conn.close()
        
        save_pending_tickets(date_str, "BRCD_KHONG_DAT", tickets)
        logging.info(f"Đã xử lý file SM4, cập nhật KPI và lưu {len(tickets)} phiếu không đạt cho ngày {date_str}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error(f"Lỗi khi xử lý file SM4 Excel: {e}")
'''

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert before 'if __name__ == '__main__':
if "if __name__ == '__main__':" in content:
    content = content.replace("if __name__ == '__main__':", func + "\n\nif __name__ == '__main__':")
else:
    content += "\n" + func

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done modifying database.py')

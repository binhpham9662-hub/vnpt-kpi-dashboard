import re
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

ttht_logic = '''
def process_ttht_excel(file_path, date_str):
    import pandas as pd
    import glob
    import os
    import logging
    
    try:
        df_ttht = pd.read_excel(file_path)
        if 'Báo Hỏng ID' in df_ttht.columns:
            df_ttht = df_ttht.rename(columns={'Báo Hỏng ID': 'BAOHONG_ID'})
            
        # Lọc ra các Báo Hỏng ID bị Trễ chuyển hạ tầng == DAT
        df_ttht['Trễ chuyển hạ tầng'] = df_ttht['Trễ chuyển hạ tầng'].astype(str).str.strip().str.upper()
        dat_ht_ids = df_ttht[df_ttht['Trễ chuyển hạ tầng'].isin(['DAT', 'ĐẠT'])]['BAOHONG_ID'].dropna().unique()
        
        # Tìm file SM4 mới nhất (loại trừ các file đã được lọc HT)
        sm4_files = [f for f in glob.glob(os.path.join('downloads', 'SM4_C11_*.xlsx')) if '_HT' not in f]
        if not sm4_files:
            logging.error("Không tìm thấy file SM4 gốc nào để lọc.")
            return
            
        latest_sm4_path = max(sm4_files, key=os.path.getctime)
        df_sm4 = pd.read_excel(latest_sm4_path)
        
        original_count = len(df_sm4)
        
        # Lọc bỏ các dòng có BAOHONG_ID nằm trong danh sách Đạt HT
        if 'BAOHONG_ID' in df_sm4.columns:
            df_sm4_filtered = df_sm4[~df_sm4['BAOHONG_ID'].isin(dat_ht_ids)]
            filtered_count = len(df_sm4_filtered)
            removed_count = original_count - filtered_count
            
            # Lưu lại thành file mới
            base_name = os.path.basename(latest_sm4_path).replace('.xlsx', '')
            new_sm4_path = os.path.join('downloads', f"{base_name}_HT.xlsx")
            df_sm4_filtered.to_excel(new_sm4_path, index=False)
            
            logging.info(f"Đã lọc bỏ {removed_count} phiếu Đạt HT khỏi {original_count} phiếu SM4 ban đầu. Lưu vào {new_sm4_path}.")
            
            # Tự động chạy lại process_sm4_excel trên file mới này để tính lại KPI và lưu DB
            # Import trực tiếp hàm process_sm4_excel (nó đã có sẵn trong database.py)
            try:
                # Gọi hàm process_sm4_excel
                process_sm4_excel(new_sm4_path, date_str)
                logging.info(f"Đã chạy lại KPI thành công bằng file {new_sm4_path}")
            except Exception as e:
                logging.error(f"Lỗi khi chạy lại process_sm4_excel: {e}")
                
        else:
            logging.error("Không tìm thấy cột BAOHONG_ID trong file SM4.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error(f"Lỗi khi xử lý file TTHT Excel và lọc file SM4: {e}")
'''

start_idx = content.find('def process_ttht_excel')
if start_idx != -1:
    new_content = content[:start_idx] + ttht_logic
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Patched database.py successfully.')
else:
    print('Could not find process_ttht_excel')

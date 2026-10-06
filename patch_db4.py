with open("database.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add the helper function right after clean_column_name
target_func = """def clean_column_name(col):
    if pd.isna(col):
        return ""
    return str(col).strip().replace('\n', ' ')"""

replacement_func = """def clean_column_name(col):
    if pd.isna(col):
        return ""
    return str(col).strip().replace('\n', ' ')

def extract_nvkt(row, zalo_account_map):
    nvkt = "Không xác định"
    
    # 1. ALWAYS PRIORITIZE TEN_KV FIRST
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
                
    # 2. FALLBACK TO NGUOI_KHOA
    if nvkt == "Không xác định" or nvkt == "":
        nguoi_khoa = str(row.get('NGUOI_KHOA', ''))
        if nguoi_khoa and nguoi_khoa.lower() != 'nan':
            nguoi_khoa = nguoi_khoa.strip(' ,')
            parts = nguoi_khoa.split('-')
            if len(parts) >= 3:
                nvkt = f"{parts[0].strip()}-{parts[-1].strip()}"
            elif len(parts) == 2:
                nvkt = f"{parts[0].strip()}-{parts[-1].strip()}"
            else:
                nvkt = nguoi_khoa
                
    # 3. FALLBACK TO TEN_NV / NGUOI_XU_LY
    if nvkt == "Không xác định" or nvkt == "":
        nvkt = str(row.get('TEN_NV', 'Không xác định'))
        if 'NGUOI_XU_LY' in row: nvkt = str(row['NGUOI_XU_LY'])
        
    return nvkt"""

content = content.replace(target_func, replacement_func)

# 1. Replace in process_and_insert_excel
target1 = """            nvkt = "Không xác định"
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
                if 'NGUOI_XU_LY' in row: nvkt = str(row['NGUOI_XU_LY'])"""

replacement1 = """            nvkt = extract_nvkt(row, zalo_account_map)"""

content = content.replace(target1, replacement1)

# 2. Replace in process_repeated_tickets_excel
target2 = """                nvkt = "Không xác định"
                nguoi_khoa = str(latest_row.get('NGUOI_KHOA', ''))
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
                    ten_kv = str(latest_row.get('TEN_KV', ''))
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
                    nvkt = str(latest_row.get('TEN_NV', 'Không xác định'))
                    if 'NGUOI_XU_LY' in latest_row: nvkt = str(latest_row['NGUOI_XU_LY'])"""

replacement2 = """                nvkt = extract_nvkt(latest_row, zalo_account_map)"""
content = content.replace(target2, replacement2)


# 3. Replace in process_sm4_excel
target3 = """            # NVKT logic
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
                if 'NGUOI_XU_LY' in row: nvkt = str(row['NGUOI_XU_LY'])"""

replacement3 = """            # NVKT logic
            nvkt = extract_nvkt(row, zalo_account_map)"""
content = content.replace(target3, replacement3)

with open("database.py", "w", encoding="utf-8") as f:
    f.write(content)

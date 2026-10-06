with open("database.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add new variables
target1 = """            total_file_sm4 += 1
            if dat_ko_hen == 1:
                total_file_sm3 += 1"""
                
replacement1 = """            total_file_sm4 += 1
            total_file_sm4_tru += (1 if not is_chuyen_ht else 0)
            if is_chuyen_ht:
                total_file_ht_dat += ht_dat
                total_file_ht_khong_dat += ht_khong_dat
            if dat_ko_hen == 1:
                total_file_sm3 += 1
                total_file_sm3_tru += (1 if not is_chuyen_ht else 0)"""

if target1 in content:
    content = content.replace(target1, replacement1)

# 2. Init new variables
target2 = """        total_file_sm3 = 0
        total_file_sm4 = 0"""

replacement2 = """        total_file_sm3 = 0
        total_file_sm4 = 0
        total_file_sm3_tru = 0
        total_file_sm4_tru = 0
        total_file_ht_dat = 0
        total_file_ht_khong_dat = 0"""

if target2 in content:
    content = content.replace(target2, replacement2)

# 3. Update query
target3 = """        # Update TOTAL row
        cursor.execute('''
            UPDATE kpi_daily SET SM3=?, SM4=? WHERE Ngay_Bao_Cao=? AND Ma_NV='TỔNG'
        ''', (total_file_sm3, total_file_sm4, date_str))"""

replacement3 = """        # Update TOTAL row
        cursor.execute('''
            UPDATE kpi_daily SET SM3=?, SM4=?, SM3_Tru=?, SM4_Tru=?, HT_Dat=?, HT_Khong_Dat=? WHERE Ngay_Bao_Cao=? AND Ma_NV='TỔNG'
        ''', (total_file_sm3, total_file_sm4, total_file_sm3_tru, total_file_sm4_tru, total_file_ht_dat, total_file_ht_khong_dat, date_str))"""

if target3 in content:
    content = content.replace(target3, replacement3)

with open("database.py", "w", encoding="utf-8") as f:
    f.write(content)

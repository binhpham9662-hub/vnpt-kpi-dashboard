with open("database.py", "r", encoding="utf-8") as f:
    content = f.read()

target1 = """            total_file_sm4 += 1
            total_file_sm4_tru += (1 if not is_chuyen_ht else 0)
            if is_chuyen_ht:
                total_file_ht_dat += ht_dat
                total_file_ht_khong_dat += ht_khong_dat
            if dat_ko_hen == 1:
                total_file_sm3 += 1
                total_file_sm3_tru += (1 if not is_chuyen_ht else 0)"""

replacement1 = """            total_file_sm4 += 1
            total_file_sm4_tru += 1 if not (dat_ko_hen == 0 and ht_dat == 1) else 0
            if is_chuyen_ht:
                total_file_ht_dat += ht_dat
                total_file_ht_khong_dat += ht_khong_dat
            if dat_ko_hen == 1:
                total_file_sm3 += 1
                total_file_sm3_tru += 1"""

content = content.replace(target1, replacement1)

target2 = """            nvkt_mapping[ma_nv_extracted]['sm4'] += 1
            nvkt_mapping[ma_nv_extracted]['sm4_tru'] += (1 if not is_chuyen_ht else 0)
            
            if is_chuyen_ht:
                nvkt_mapping[ma_nv_extracted]['ht_dat'] += ht_dat
                nvkt_mapping[ma_nv_extracted]['ht_khong_dat'] += ht_khong_dat
                
            if dat_ko_hen == 1:
                nvkt_mapping[ma_nv_extracted]['sm3'] += 1
                nvkt_mapping[ma_nv_extracted]['sm3_tru'] += (1 if not is_chuyen_ht else 0)"""

replacement2 = """            nvkt_mapping[ma_nv_extracted]['sm4'] += 1
            nvkt_mapping[ma_nv_extracted]['sm4_tru'] += 1 if not (dat_ko_hen == 0 and ht_dat == 1) else 0
            
            if is_chuyen_ht:
                nvkt_mapping[ma_nv_extracted]['ht_dat'] += ht_dat
                nvkt_mapping[ma_nv_extracted]['ht_khong_dat'] += ht_khong_dat
                
            if dat_ko_hen == 1:
                nvkt_mapping[ma_nv_extracted]['sm3'] += 1
                nvkt_mapping[ma_nv_extracted]['sm3_tru'] += 1"""

content = content.replace(target2, replacement2)

with open("database.py", "w", encoding="utf-8") as f:
    f.write(content)

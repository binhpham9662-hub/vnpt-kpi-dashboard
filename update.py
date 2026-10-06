with open("database.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """            dat_ko_hen = row.get('DAT_KO_HEN', 0)
            
            total_file_sm4 += 1
            if dat_ko_hen == 1:
                total_file_sm3 += 1
            
            if ma_nv_extracted not in nvkt_mapping:
                nvkt_mapping[ma_nv_extracted] = {'ten': ten_nv_extracted, 'to': to_ktdb, 'sm3': 0, 'sm4': 0}
                
            nvkt_mapping[ma_nv_extracted]['sm4'] += 1
            if dat_ko_hen == 1:
                nvkt_mapping[ma_nv_extracted]['sm3'] += 1
            else:"""

replacement = """            dat_ko_hen = row.get('DAT_KO_HEN', 0)
            tg_chuyen_ht = row.get('thời gian ttvt mới chuyển về hạ tầng lần đầu')
            tg_qd = row.get('THOIGIAN_QD_KO_HEN')
            
            is_chuyen_ht = False
            ht_dat = 0
            ht_khong_dat = 0
            
            if pd.notna(tg_chuyen_ht) and str(tg_chuyen_ht).strip() != '':
                is_chuyen_ht = True
                try:
                    tg_chuyen_val = float(tg_chuyen_ht)
                    tg_qd_val = float(tg_qd)
                    if tg_chuyen_val < 0.5 * tg_qd_val:
                        ht_dat = 1
                    else:
                        ht_khong_dat = 1
                except:
                    ht_khong_dat = 1
            
            total_file_sm4 += 1
            if dat_ko_hen == 1:
                total_file_sm3 += 1
            
            if ma_nv_extracted not in nvkt_mapping:
                nvkt_mapping[ma_nv_extracted] = {
                    'ten': ten_nv_extracted, 
                    'to': to_ktdb, 
                    'sm3': 0, 
                    'sm4': 0,
                    'ht_dat': 0,
                    'ht_khong_dat': 0,
                    'sm3_tru': 0,
                    'sm4_tru': 0
                }
                
            nvkt_mapping[ma_nv_extracted]['sm4'] += 1
            nvkt_mapping[ma_nv_extracted]['sm4_tru'] += (1 if not is_chuyen_ht else 0)
            
            if is_chuyen_ht:
                nvkt_mapping[ma_nv_extracted]['ht_dat'] += ht_dat
                nvkt_mapping[ma_nv_extracted]['ht_khong_dat'] += ht_khong_dat
                
            if dat_ko_hen == 1:
                nvkt_mapping[ma_nv_extracted]['sm3'] += 1
                nvkt_mapping[ma_nv_extracted]['sm3_tru'] += (1 if not is_chuyen_ht else 0)
            else:"""

content = content.replace(target, replacement)

target2 = """        save_pending_tickets(date_str, "BRCD_KHONG_DAT", tickets)
        logging.info(f"Đã xử lý file SM4, cập nhật KPI và lưu {len(tickets)} phiếu không đạt cho ngày {date_str}")"""

replacement2 = """        save_pending_tickets(date_str, "BRCD_KHONG_DAT", tickets)
        logging.info(f"Đã xử lý file SM4, cập nhật KPI và lưu {len(tickets)} phiếu không đạt cho ngày {date_str}")

        # TẠO REPORT EXCEL MỚI
        report_data = []
        for ma_nv, data in nvkt_mapping.items():
            if ma_nv == "Không xác định" or not ma_nv: continue
            sm3 = data['sm3']
            sm4 = data['sm4']
            ty_le = f"{(sm3/sm4)*100:.2f}%" if sm4 > 0 else "0%"
            
            sm3_tru = data['sm3_tru']
            sm4_tru = data['sm4_tru']
            ty_le_tru = f"{(sm3_tru/sm4_tru)*100:.2f}%" if sm4_tru > 0 else "0%"
            
            report_data.append({
                "Tên Đội": data['to'],
                "Mã NV": ma_nv,
                "Tên NV": data['ten'],
                "SM4": sm4,
                "SM3": sm3,
                "Tỷ lệ": ty_le,
                "SL phiếu đã chuyển HT đạt": data['ht_dat'],
                "SL phiếu đã chuyển HT không đạt": data['ht_khong_dat'],
                "Tỷ lệ đạt sau giảm trừ lỗi do hạ tầng": ty_le_tru
            })
            
        report_df = pd.DataFrame(report_data)
        import os
        report_filename = f"Ty_Le_SM4_Giam_Tru_HT_{date_str.replace('-', '')}.xlsx"
        report_filepath = os.path.join(os.path.dirname(file_path), report_filename)
        report_df.to_excel(report_filepath, index=False)
        logging.info(f"Đã tạo file báo cáo tỷ lệ SM4 tại {report_filepath}")
        
        return report_filepath"""

content = content.replace(target2, replacement2)

with open("database.py", "w", encoding="utf-8") as f:
    f.write(content)

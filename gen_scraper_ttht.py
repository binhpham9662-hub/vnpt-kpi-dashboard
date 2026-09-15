import sys
import re

file_path = r'H:\web-bao-cao\scraper.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('def run_download_sm4():')
end_idx = content.find('def listen_for_triggers():')
if start_idx != -1 and end_idx != -1:
    sm4_func = content[start_idx:end_idx]
    
    ttht_func = sm4_func.replace('run_download_sm4', 'run_download_ttht')
    ttht_func = ttht_func.replace('https://baocao.hanoi.vnpt.vn/report/report-info?id=494793&menu_id=494801', 'https://baocao.hanoi.vnpt.vn/report/report-info?id=538247&menu_id=538272')
    
    # Remove the Loai phieu section
    ttht_func = re.sub(r'\s*logging\.info\(\"Chọn Loại phiếu...\"\).*?except Exception as e:\s+logging\.error\(f\"Lỗi khi chọn Loại phiếu: \{e\}\"\)', '', ttht_func, flags=re.DOTALL)
    
    ttht_func = ttht_func.replace('SM4_C11_', 'TTHT_')
    ttht_func = ttht_func.replace('SM4 C11 2026', 'TTHT xử lý')
    ttht_func = ttht_func.replace('process_sm4_excel', 'process_ttht_excel')
    
    print('Generated run_download_ttht successfully')
    
    new_content = content[:end_idx] + ttht_func + '\n' + content[end_idx:]
    
    # add to trigger
    trigger_logic_old = '''            elif msg == "RUN_SM4":
                logging.info("Thực thi lấy Báo cáo BRCĐ Không tính hẹn SM4 theo yêu cầu từ Web...")
                try:
                    run_download_sm4()
                except Exception as e:
                    logging.error(f"Lỗi khi chạy SM4: {e}")'''
    trigger_logic_new = trigger_logic_old + '''
            elif msg == "RUN_TTHT":
                logging.info("Thực thi lấy Báo cáo TTHT theo yêu cầu từ Web...")
                try:
                    run_download_ttht()
                except Exception as e:
                    logging.error(f"Lỗi khi chạy TTHT: {e}")'''
    
    new_content = new_content.replace(trigger_logic_old, trigger_logic_new)
    new_content = new_content.replace('["RUN_KPI", "RUN_SM1", "RUN_SM4"]', '["RUN_KPI", "RUN_SM1", "RUN_SM4", "RUN_TTHT"]')
    
    with open('H:\\web-bao-cao\\scraper.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Saved to scraper.py')
else:
    print('Could not find boundaries')

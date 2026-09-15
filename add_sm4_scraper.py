import sys
import re

file_path = r'H:\web-bao-cao\scraper.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract run_download_sm1
match = re.search(r'(def run_download_sm1\(\):.*?browser\.close\(\)\n)', content, re.DOTALL)
if not match:
    print('Could not find run_download_sm1')
    sys.exit(1)

sm1_func = match.group(1)

# 2. Create run_download_sm4
sm4_func = sm1_func.replace('run_download_sm1', 'run_download_sm4')
sm4_func = sm4_func.replace('SM1 C12 2026', 'SM4 C11 2026')
sm4_func = sm4_func.replace('SM1_C12_', 'SM4_C11_')
sm4_func = sm4_func.replace('SM1 C12', 'SM4 C11')
sm4_func = sm4_func.replace('process_repeated_tickets_excel', 'process_sm4_excel')

# Insert sm4_func right after sm1_func
new_content = content.replace(sm1_func, sm1_func + '\n' + sm4_func)

# 3. Add to triggers
trigger_logic_old = '''            elif msg == "RUN_SM1":
                logging.info("Thực thi lấy Báo cáo Hỏng Lặp SM1 theo yêu cầu từ Web...")
                try:
                    run_download_sm1()
                except Exception as e:
                    logging.error(f"Lỗi khi chạy SM1: {e}")'''
                    
trigger_logic_new = trigger_logic_old + '''
            elif msg == "RUN_SM4":
                logging.info("Thực thi lấy Báo cáo BRCĐ Không tính hẹn SM4 theo yêu cầu từ Web...")
                try:
                    run_download_sm4()
                except Exception as e:
                    logging.error(f"Lỗi khi chạy SM4: {e}")'''

new_content = new_content.replace(trigger_logic_old, trigger_logic_new)
new_content = new_content.replace('["RUN_KPI", "RUN_SM1"]', '["RUN_KPI", "RUN_SM1", "RUN_SM4"]')

# 4. Add to schedule
schedule_old = 'schedule.every().day.at("08:15").do(run_download_sm1)'
schedule_new = schedule_old + '\n    schedule.every().day.at("08:20").do(run_download_sm4)'
new_content = new_content.replace(schedule_old, schedule_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done modifying scraper.py')

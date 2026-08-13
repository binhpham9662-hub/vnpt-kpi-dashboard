import sys
with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith('def sync_overdue_pttb():'):
        new_lines.append('def sync_overdue_pttb():\n')
        new_lines.append('    logging.info("Bắt đầu đồng bộ phiếu tồn PTTB...")\n')
        new_lines.append('    from database import sync_pttb_from_json\n')
        new_lines.append('    try:\n')
        new_lines.append('        sync_pttb_from_json()\n')
        new_lines.append('        logging.info("Đã đồng bộ phiếu tồn PTTB thành công.")\n')
        new_lines.append('    except Exception as e:\n')
        new_lines.append('        logging.error(f"Lỗi khi đồng bộ PTTB: {e}")\n\n')
        skip = True
        continue
    
    if skip:
        if line.startswith('def get_report_dates():') or line.startswith('def run_download_sm1():'):
            skip = False
        else:
            continue
            
    new_lines.append(line)

with open(r'H:\web-bao-cao\scraper.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

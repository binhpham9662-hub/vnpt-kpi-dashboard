with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    with open('debug_sync_pttb.txt', 'w', encoding='utf-8') as out:
        in_func = False
        for line in f:
            if 'Bắt đầu đồng bộ phiếu tồn PTTB' in line:
                in_func = True
            if in_func:
                out.write(line)
                if line.startswith('def ') and 'sync_daily' not in line:
                    break

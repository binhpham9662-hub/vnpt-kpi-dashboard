with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    with open('H:\\web-bao-cao\\sync_pttb.txt', 'w', encoding='utf-8') as out:
        in_func = False
        for line in f:
            if 'def sync_overdue_pttb' in line:
                in_func = True
            if in_func:
                out.write(line)
                if 'push_to_github' in line:
                    break

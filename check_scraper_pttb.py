with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    with open('debug_scraper_pttb.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(f):
            if 'PTTB' in line or 'bao_cao_onebss.xlsx' in line or 'database' in line:
                out.write(f'Line {i+1}: {line}')

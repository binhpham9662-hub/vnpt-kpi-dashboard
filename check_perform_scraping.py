with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    with open('debug_perform_scraping.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def perform_scraping(' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'perform_scraping' in line:
                    break

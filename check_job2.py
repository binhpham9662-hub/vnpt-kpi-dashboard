with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    with open('debug_job2.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def job_crawl_and_report' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'job_crawl_and_report' in line:
                    break

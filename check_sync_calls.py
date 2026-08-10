with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    with open('debug_sync_calls.txt', 'w', encoding='utf-8') as out:
        lines = f.readlines()
        for i in [284, 508]:
            for j in range(max(0, i-10), min(len(lines), i+10)):
                out.write(f'Line {j+1}: {lines[j]}')
            out.write('---\n')

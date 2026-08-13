with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8', errors='ignore') as f:
    with open('H:\\web-bao-cao\\ntfy_lines.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(f):
            if 'ntfy.sh' in line:
                out.write(f'Line {i+1}: {line}')

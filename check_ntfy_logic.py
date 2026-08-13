with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    with open('H:\\web-bao-cao\\ntfy_logic.txt', 'w', encoding='utf-8') as out:
        for i in range(540, min(580, len(lines))):
            out.write(f'Line {i+1}: {lines[i]}')

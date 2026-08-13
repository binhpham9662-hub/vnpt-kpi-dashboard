with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    with open(r'H:\web-bao-cao\search_out.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(f):
            if 'tồn pttb' in line.lower() or 'tổng hợp' in line.lower():
                out.write(f'Line {i+1}: {line}')

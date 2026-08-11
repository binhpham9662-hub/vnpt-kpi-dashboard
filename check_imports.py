with open(r'h:\vnpt_report\app.py', 'r', encoding='utf-8-sig') as f:
    with open('H:\\web-bao-cao\\debug_imports.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(f):
            if 'import' in line:
                out.write(f'Line {i+1}: {line}')

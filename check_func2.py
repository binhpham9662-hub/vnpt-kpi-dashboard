with open(r'h:\vnpt_report\app.py', 'r', encoding='utf-8', errors='ignore') as f:
    with open('H:\\web-bao-cao\\debug_func2.txt', 'w', encoding='utf-8') as out:
        in_func = False
        for i, line in enumerate(f):
            if 'def process_sm2_report' in line:
                in_func = True
                out.write(f'Line {i+1}: {line}')
            elif in_func and line.startswith('def '):
                in_func = False
            elif in_func:
                out.write(f'Line {i+1}: {line}')

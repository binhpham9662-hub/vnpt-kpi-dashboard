with open(r'h:\vnpt_report\app.py', 'r', encoding='utf-8-sig', errors='ignore') as f:
    for i, line in enumerate(f):
        if 'BRCD_LAP' in line or 'process_repeated' in line or 'database' in line:
            print(f'Line {i+1}: {line.strip()}')

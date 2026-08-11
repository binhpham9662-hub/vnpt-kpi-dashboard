with open(r'h:\vnpt_report\app.py', 'r', encoding='utf-8-sig') as f:
    with open('H:\\web-bao-cao\\debug_db.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(f):
            if 'kpi_history.db' in line or 'sqlite3' in line or 'insert' in line.lower():
                out.write(f'Line {i+1}: {line}')

with open(r'H:\web-bao-cao\database.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'nguoi_khoa = str(latest_row.get(\'NGUOI_KHOA\', \'\'))' in line:
            with open('debug_db_replace.txt', 'w', encoding='utf-8') as out:
                for j in range(i-2, i+15):
                    out.write(f'Line {j+1}: {lines[j]}')
            break

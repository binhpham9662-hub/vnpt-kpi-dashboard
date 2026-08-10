with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'details_df = get_pending_details(start_date, end_date, loai_phieu, level, value)' in line:
            with open('debug_get_pending_details_app.txt', 'a', encoding='utf-8') as out:
                for j in range(i, min(len(lines), i+15)):
                    out.write(f'Line {j+1}: {lines[j]}')
                out.write('---\n')
        elif 'details_df = get_pending_details(start_date, end_date, loai_phieu, "CENTER", "")' in line:
            with open('debug_get_pending_details_app.txt', 'a', encoding='utf-8') as out:
                for j in range(i, min(len(lines), i+15)):
                    out.write(f'Line {j+1}: {lines[j]}')
                out.write('---\n')

with open(r'H:\web-bao-cao\database.py', 'r', encoding='utf-8') as f:
    with open('debug_get_kpi.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def get_kpi_for_date(' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'get_kpi_for_date' in line:
                    break

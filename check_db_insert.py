with open(r'H:\web-bao-cao\database.py', 'r', encoding='utf-8') as f:
    with open('debug_db_insert.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def process_and_insert_excel' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'process_and_insert_excel' in line:
                    break

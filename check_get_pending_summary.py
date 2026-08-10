with open(r'H:\web-bao-cao\database.py', 'r', encoding='utf-8') as f:
    with open('debug_get_pending_summary.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def get_pending_summary' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'get_pending_summary' in line:
                    break

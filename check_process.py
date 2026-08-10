with open(r'h:\vnpt_report\app.py', 'r', encoding='utf-8') as f:
    with open('debug_process.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def process_data_and_report' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'process_data_and_report' in line:
                    break

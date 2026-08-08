with open(r'h:\vnpt_report\app.py', 'r', encoding='utf-8') as f:
    with open('debug_app.txt', 'w', encoding='utf-8') as out:
        in_func = False
        for line in f:
            if line.startswith('def run_onebss_report_with_retries'):
                in_func = True
            if in_func:
                out.write(line)
                if line.startswith('def ') and not line.startswith('def run_onebss_report_with_retries'):
                    break

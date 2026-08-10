with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'if msg == "RUN_KPI":' in line or 'if msg in ["RUN_KPI", "RUN_SM1"]:' in line:
            with open('debug_run_kpi.txt', 'a', encoding='utf-8') as out:
                for j in range(i, min(i+20, len(lines))):
                    out.write(f'Line {j+1}: {lines[j]}')

with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    with open('debug_app_btn.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for i, line in enumerate(f):
            if 'Lấy Báo Cáo Tổng Quan KPI' in line:
                in_block = True
            if in_block:
                out.write(f'Line {i+1}: {line}')
                if 'st.sidebar.button' in line and not 'Lấy Báo Cáo Tổng Quan KPI' in line:
                    break

with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    with open('debug_repeated.txt', 'w', encoding='utf-8') as out:
        for i, line in enumerate(f):
            if 'repeated_tickets' in line or 'Hỏng Lặp' in line or 'hong_lap' in line or 'brcd_lap' in line or 'def show_pending_brcd_lap' in line or 'def get_repeated_tickets' in line:
                out.write(f'Line {i+1}: {line}')

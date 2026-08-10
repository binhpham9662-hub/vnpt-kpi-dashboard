with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    with open('debug_render_pending.txt', 'w', encoding='utf-8') as out:
        in_block = False
        for line in f:
            if 'def render_pending_tickets_page(' in line:
                in_block = True
            if in_block:
                out.write(line)
                if line.startswith('def ') and not 'render_pending_tickets_page' in line:
                    break

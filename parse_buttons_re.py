import re

with open('debug_new_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

items = re.findall(r'<([a-zA-Z0-9]+)[^>]*>(.*?)</\1>', html, re.IGNORECASE | re.DOTALL)
with open('output.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(items):
        tag, text = item
        text = text.strip()
        if 'excel' in text.lower() or 'dữ liệu' in text.lower() or 'li?u' in text.lower() or 't?t' in text.lower() or 'tất' in text.lower():
            out.write(f"Tag: {tag} - text: '{text}'\n")

import re

html = open('debug_new_page.html', encoding='utf-8').read()
matches = re.finditer(r'.{0,100}dang xem.{0,100}', html, re.IGNORECASE)
with open('output_search.txt', 'w', encoding='utf-8') as f:
    for m in matches:
        f.write(m.group(0) + '\n---\n')

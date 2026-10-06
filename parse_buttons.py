from bs4 import BeautifulSoup

with open('debug_new_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

for i, btn in enumerate(soup.find_all(['button', 'a'])):
    cls = btn.get('class')
    text = btn.text.strip()
    if 'excel' in text.lower() or 'dữ liệu' in text.lower() or 'tất cả' in text.lower():
        print(f"Index {i} - tag: {btn.name}, class: {cls}, text: '{text}'")

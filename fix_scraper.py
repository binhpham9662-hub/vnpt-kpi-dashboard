import re
with open('scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('def run_download_ttht():')
end_idx = content.find('def listen_for_triggers():')

ttht_func = content[start_idx:end_idx]

# Replace URL
ttht_func = ttht_func.replace('id=267215&menu_id=276194', 'id=538247&menu_id=538272')

# Remove Loai phieu
match = re.search(r'\s*logging\.info\(\"Chọn Loại phiếu.*?except Exception as e:\s+logging\.error\(f\"Lỗi khi chọn Loại phiếu: \{e\}\"\)', ttht_func, flags=re.DOTALL)
if match:
    ttht_func = ttht_func[:match.start()] + ttht_func[match.end():]
else:
    print('Could not find Loại phiếu block')

new_content = content[:start_idx] + ttht_func + content[end_idx:]

with open('scraper.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Fixed scraper.py')

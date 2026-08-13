import sys

with open(r'H:\web-bao-cao\scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')",
    "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('scraper_run.log', encoding='utf-8'), logging.StreamHandler(sys.stdout)])"
)

with open(r'H:\web-bao-cao\scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

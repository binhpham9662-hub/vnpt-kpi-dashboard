with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """# Initialize DB on first run if not exists
if not os.path.exists('kpi_history.db'):
    init_db()"""

replacement = """# Initialize DB on first run if not exists
if not os.path.exists('kpi_history.db'):
    init_db()

# Auto patch missing columns on startup
try:
    import patch_db
    patch_db.patch_database()
except Exception as e:
    pass"""

if target in content:
    content = content.replace(target, replacement)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

import importlib
import database
importlib.reload(database)

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

if "importlib.reload(database)" not in content:
    content = content.replace("from database import get_kpi_for_date, init_db, get_pending_summary, get_pending_details",
                              "from database import get_kpi_for_date, init_db, get_pending_summary, get_pending_details\nimport importlib\nimport database\nimportlib.reload(database)")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

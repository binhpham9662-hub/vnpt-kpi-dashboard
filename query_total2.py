import sqlite3
import json

conn = sqlite3.connect('kpi_history.db')
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT * FROM kpi_daily WHERE Ma_NV='TỔNG'").fetchall()
with open("total_row.json", "w", encoding="utf-8") as f:
    f.write(json.dumps([dict(ix) for ix in rows], indent=4, ensure_ascii=False))
conn.close()

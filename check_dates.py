import sqlite3
import pandas as pd
conn = sqlite3.connect('kpi_history.db')
print(pd.read_sql_query("SELECT Ngay_Bao_Cao, Loai_Phieu, COUNT(*) as Count FROM pending_tickets GROUP BY Ngay_Bao_Cao, Loai_Phieu ORDER BY Ngay_Bao_Cao DESC LIMIT 10", conn))

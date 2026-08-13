import sqlite3
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

conn = sqlite3.connect(r'H:\web-bao-cao\kpi_history.db')
c = conn.cursor()
c.execute("SELECT DISTINCT Ly_Do_Ton FROM pending_tickets WHERE Loai_Phieu='PTTB' LIMIT 10")
print('PTTB Ly_Do_Ton:', c.fetchall())
c.execute("SELECT DISTINCT Ly_Do_Ton FROM pending_tickets WHERE Loai_Phieu='BHSC' LIMIT 10")
print('BHSC Ly_Do_Ton:', c.fetchall())

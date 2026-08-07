import sqlite3
conn = sqlite3.connect('kpi_history.db')
c = conn.cursor()
c.execute("SELECT rowid, Ly_Do_Ton FROM pending_tickets WHERE Loai_Phieu='BRCD_LAP'")
rows = c.fetchall()
for rowid, text in rows:
    if text:
        new_text = text.replace('<b>', '').replace('</b>', '').replace('<br>', '\n')
        c.execute('UPDATE pending_tickets SET Ly_Do_Ton=? WHERE rowid=?', (new_text, rowid))
conn.commit()
conn.close()
print('Fixed HTML tags in database')

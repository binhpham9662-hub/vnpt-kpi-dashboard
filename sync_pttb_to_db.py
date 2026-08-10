import json
import sqlite3

def sync_pttb():
    file_path = r'H:\vnpt_report\daily_overdue_pttb.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print('Error reading JSON:', e)
        return

    conn = sqlite3.connect(r'H:\web-bao-cao\kpi_history.db')
    c = conn.cursor()
    
    for date_str, tickets in data.items():
        # Check if this date already exists for PTTB
        c.execute("SELECT COUNT(*) FROM pending_tickets WHERE Ngay_Bao_Cao=? AND Loai_Phieu='PTTB'", (date_str,))
        count = c.fetchone()[0]
        if count == 0:
            print(f'Syncing {len(tickets)} PTTB tickets for {date_str}...')
            for ma_tb, t_info in tickets.items():
                c.execute("""
                    INSERT INTO pending_tickets 
                    (Ngay_Bao_Cao, Loai_Phieu, Ma_TB, To_KTDB, NVKT, Gio_Ton, Ly_Do_Ton)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    date_str, 
                    'PTTB',
                    ma_tb,
                    t_info.get('Tổ', ''),
                    t_info.get('NVKT', ''),
                    float(t_info.get('GIO_TON', 0) or 0),
                    t_info.get('LY_DO_TON', '')
                ))
    conn.commit()
    conn.close()
    print('Sync complete.')

sync_pttb()

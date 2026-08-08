import pandas as pd
import logging
import sqlite3

zalo_df = pd.read_excel(r'H:\vnpt_report\zalo.xlsx')
zalo_df['Account'] = zalo_df['Account'].astype(str).str.strip().str.upper()
zalo_account_map = dict(zip(zalo_df['Account'], zalo_df['MA_NV']))

test_cases = [
    'DAH-PTH-KHANHPC.HNI(Nguyên Khê; T.hùng;x.nguyễn;x.núi)',
    'DAH-DAH-LMHUNG.HNI( Phúc Lộc, Đài Bi, NGHĨA LẠI)',
    'DAH-DAH-THANNHDX.HNI(X.CHỢ; X.hậu;x.ngoài;x.thượng;x.trong)'
]

with open('debug_test_parsing.txt', 'w', encoding='utf-8') as f:
    for ten_kv in test_cases:
        nvkt = "Không xác định"
        if ten_kv and '(' in ten_kv:
            prefix = ten_kv.split('(')[0]
            parts = prefix.split('-')
            if len(parts) > 0:
                account = parts[-1].strip().upper()
                if account in zalo_account_map:
                    nvkt = zalo_account_map[account]
                else:
                    f.write(f"FAILED: {account} not in map\n")
        f.write(f"TEN_KV: {ten_kv}\n")
        f.write(f"NVKT: {nvkt}\n\n")

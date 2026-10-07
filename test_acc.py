import pandas as pd
import database
import json

zalo_df = pd.read_excel('zalo.xlsx')
zalo_account_map = {}
if 'Account' in zalo_df.columns:
    zalo_df['Account'] = zalo_df['Account'].astype(str).str.strip().str.upper()
    zalo_account_map = dict(zip(zalo_df['Account'], zalo_df['MA_NV']))

row_quannh = {'TEN_KV': 'DAH-MLH-QUANNH(YEN MAC XA LIEN MAC)', 'NGUOI_KHOA': 'VNPT016629-thont-Nguyễn Trường Thọ'}
res_quannh = database.extract_nvkt(row_quannh, zalo_account_map)

row_trungnt1 = {'TEN_KV': 'DAH-MLH-TRUNGNT1(YEN MAC XA LIEN MAC)', 'NGUOI_KHOA': 'VNPT016629-thont-Nguyễn Trường Thọ'}
res_trungnt1 = database.extract_nvkt(row_trungnt1, zalo_account_map)

with open('test_accounts_res.txt', 'w', encoding='utf-8') as f:
    f.write(f"quannh -> {res_quannh}\n")
    f.write(f"trungnt1 -> {res_trungnt1}\n")

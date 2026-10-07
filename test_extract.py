import pandas as pd
import database

# Load zalo map as the database does
zalo_df = pd.read_excel('zalo.xlsx')
zalo_account_map = {}
if 'Account' in zalo_df.columns:
    zalo_df['Account'] = zalo_df['Account'].astype(str).str.strip().str.upper()
    zalo_account_map = dict(zip(zalo_df['Account'], zalo_df['MA_NV']))

with open('test_res.txt', 'w', encoding='utf-8') as f:
    # Test
    row1 = {'TEN_KV': 'DAH-MLH-SYDQ(CAM VAN, TIEN DAI, TRUNG XUAN, VAN PHUC, YEN NOI XA VAN YEN)', 'NGUOI_KHOA': 'VNPT016629-thont-Nguyễn Trường Thọ'}
    f.write("Test SYDQ: " + database.extract_nvkt(row1, zalo_account_map) + "\n")

    row2 = {'TEN_KV': 'DAH-MLH-CHUNGNT1(Mê Linh: Hạ Lôi)', 'NGUOI_KHOA': 'VNPT016629-thont-Nguyễn Trường Thọ'}
    f.write("Test CHUNGNT1: " + database.extract_nvkt(row2, zalo_account_map) + "\n")

    row_empty = {'TEN_KV': '', 'NGUOI_KHOA': 'VNPT016629-thont-Nguyễn Trường Thọ'}
    f.write("Test empty: " + database.extract_nvkt(row_empty, zalo_account_map) + "\n")

    row_no_paren = {'TEN_KV': 'DAH-MLH-SYDQ', 'NGUOI_KHOA': 'VNPT016629-thont-Nguyễn Trường Thọ'}
    f.write("Test no paren: " + database.extract_nvkt(row_no_paren, zalo_account_map) + "\n")

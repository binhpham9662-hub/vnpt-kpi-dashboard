import pandas as pd
import glob
import os

files = glob.glob(r'H:\web-bao-cao\downloads\SM1_C12_*.xlsx')
latest_file = max(files, key=os.path.getctime)
df = pd.read_excel(latest_file)

counts = df['MA_TB'].value_counts()
repeated_df = df[df['MA_TB'].isin(counts[counts >= 2].index)].copy()
latest_df = repeated_df.groupby('MA_TB', as_index=False).first()

zalo_df = pd.read_excel(r'H:\vnpt_report\zalo.xlsx')
zalo_df['Account'] = zalo_df['Account'].astype(str).str.strip().str.upper()
zalo_account_map = dict(zip(zalo_df['Account'], zalo_df['MA_NV']))

for _, row in latest_df.iterrows():
    ten_kv = str(row.get('TEN_KV', ''))
    account = ''
    if ten_kv and '(' in ten_kv:
        account = ten_kv.split('(')[0].split('-')[-1].strip().upper()
    if account and account not in zalo_account_map:
        print(f"Missing account in Zalo: {account} (from {ten_kv})")
    elif not account:
        print(f"Could not extract account from TEN_KV: {ten_kv}")

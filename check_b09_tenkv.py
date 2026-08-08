import pandas as pd
import glob
import os

files = glob.glob(r'H:\web-bao-cao\downloads\SM1_C12_*.xlsx')
latest_file = max(files, key=os.path.getctime)
df = pd.read_excel(latest_file)
missing = df[df['MA_TB'] == 'b0912300443']
with open('debug_b09_tenkv.txt', 'w', encoding='utf-8') as f:
    for idx, row in missing.iterrows():
        f.write(f"{row['NGAY_BAO_HONG']} | TEN_KV: {row.get('TEN_KV', 'NOT_FOUND')}\n")

import pandas as pd
import glob
import os

files = glob.glob(r'H:\web-bao-cao\downloads\SM1_C12_*.xlsx')
latest_file = max(files, key=os.path.getctime)
df = pd.read_excel(latest_file)

with open('debug_ten_kv.txt', 'w', encoding='utf-8') as f:
    f.write('Columns: ' + str(df.columns.tolist()) + '\n')
    missing = df[df['MA_TB'].isin(['b0912300443', 'ctythanglonghni', 'bibo6868'])]
    for _, row in missing.iterrows():
        f.write(str(row['MA_TB']) + ' | TEN_KV: ' + str(row.get('TEN_KV', 'NOT_FOUND')) + '\n')

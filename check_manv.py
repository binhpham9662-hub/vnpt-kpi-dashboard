import pandas as pd
df = pd.read_excel(r'H:\vnpt_report\zalo.xlsx')
matches = df[df['Account'].astype(str).str.contains('LMHUNG|THANNHDX', case=False, na=False)]
with open('debug_manv.txt', 'w', encoding='utf-8') as f:
    for _, row in matches.iterrows():
        f.write(f"{row['Account']} -> {row['MA_NV']}\n")

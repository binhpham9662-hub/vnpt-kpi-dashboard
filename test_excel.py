import pandas as pd
import os

files = [f for f in os.listdir(r'H:\vnpt_report') if 'SM4' in f]
print(files)
if not files:
    print("No SM4 files found.")
else:
    latest_file = os.path.join(r'H:\vnpt_report', max(files, key=lambda f: os.path.getctime(os.path.join(r'H:\vnpt_report', f))))
    print("Reading", latest_file)
    df = pd.read_excel(latest_file)
    
    header_row_idx = None
    for i, row in df.iterrows():
        row_str = " ".join([str(v).lower() for v in row.values])
        if 'mã nhân viên' in row_str or 'đơn vị' in row_str or 'sm4' in row_str:
            header_row_idx = i
            break
            
    if header_row_idx is not None:
        df = pd.read_excel(latest_file, header=header_row_idx+1)
        
    print("Total rows:", len(df))
    if 'SM4' in df.columns:
        df['SM4'] = pd.to_numeric(df['SM4'], errors='coerce').fillna(0)
        df['SM3'] = pd.to_numeric(df['SM3'], errors='coerce').fillna(0)
        print("Sum SM4:", df['SM4'].sum())
        print("Sum SM3:", df['SM3'].sum())
        print("SM4 - SM3:", df['SM4'].sum() - df['SM3'].sum())
        
    if 'DAT_KO_HEN' in df.columns:
        print("Count DAT_KO_HEN == 'Không đạt':", len(df[df['DAT_KO_HEN'] == 'Không đạt']))
        print("Count DAT_KO_HEN == 'Đạt':", len(df[df['DAT_KO_HEN'] == 'Đạt']))
        print("Count DAT_KO_HEN == 'Chưa tính hẹn':", len(df[df['DAT_KO_HEN'] == 'Chưa tính hẹn']))
        print("Unique values in DAT_KO_HEN:")
        print(df['DAT_KO_HEN'].value_counts(dropna=False))
        
        missing_df = df[(df['SM4'] > df['SM3']) & (df['DAT_KO_HEN'] != 'Không đạt')]
        print("\nTickets with SM4 > SM3 but DAT_KO_HEN is not 'Không đạt':")
        if not missing_df.empty:
            print(missing_df[['MÃ THUÊ BAO', 'DAT_KO_HEN', 'SM4', 'SM3']])
        else:
            print("None")

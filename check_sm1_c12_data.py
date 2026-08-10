import pandas as pd
import glob
files = glob.glob(r'H:\web-bao-cao\downloads\SM1_C12_*.xlsx')
if files:
    latest_file = sorted(files)[-1]
    df = pd.read_excel(latest_file)
    with open('debug_sm1_c12_data.txt', 'w', encoding='utf-8') as f:
        f.write(str(df.columns.tolist()) + '\n')
        f.write(str(df.head().to_dict('records')))
else:
    with open('debug_sm1_c12_data.txt', 'w', encoding='utf-8') as f:
        f.write('No SM1_C12 files found')

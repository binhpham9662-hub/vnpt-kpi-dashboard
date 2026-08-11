import sys
sys.path.append('H:\\web-bao-cao')
from database import process_repeated_tickets_excel
import pandas as pd

file_path = "H:\\web-bao-cao\\downloads\\SM1_C12_20260811_081557.xlsx"
df = pd.read_excel(file_path)

for _, row in df.iterrows():
    print(row.get('NGUOI_KHOA', 'N/A'))
    break

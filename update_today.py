from database import process_sm4_excel
import glob
import os
from datetime import datetime

# Find latest SM4 file
files = glob.glob(r'H:\web-bao-cao\downloads\SM4_C11_*.xlsx')
latest_file = max(files, key=os.path.getctime)

today_str = datetime.now().strftime("%Y-%m-%d")
print(f"Processing {latest_file} for date {today_str}")

process_sm4_excel(latest_file, today_str)
print("Done.")

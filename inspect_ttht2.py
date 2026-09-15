import pandas as pd
import json
df = pd.read_excel(r'H:\web-bao-cao\downloads\TTHT_20260915_164059.xlsx')
cols = df.columns.tolist()
print(json.dumps(cols, ensure_ascii=False))
print(df.head(2).to_dict('records'))

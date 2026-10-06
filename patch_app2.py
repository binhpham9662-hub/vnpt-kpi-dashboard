with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """            'SL phiếu đã chuyển HT đạt': brcd_agg['Tong_HT_Dat'],
            'SL phiếu đã chuyển HT không đạt': brcd_agg['Tong_HT_Khong_Dat'],"""

replacement = """            'SL phiếu đã chuyển HT đạt': brcd_agg['Tong_HT_Dat'],
            'SL phiếu đã chuyển HT không đạt': brcd_agg['Tong_HT_Khong_Dat'],
            'Phiếu K.Đạt lỗi do HT': brcd_agg['Tong_SM4'] - brcd_agg['Tong_SM4_Tru'],"""

content = content.replace(target, replacement)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

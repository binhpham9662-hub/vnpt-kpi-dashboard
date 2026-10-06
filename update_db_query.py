with open("database.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("t.SM1, t.SM2, t.SM3, t.SM4, t.SM5, t.SM6, t.SM4_Dat_HT, t.SM4_Khong_Dat_HT,", "t.SM1, t.SM2, t.SM3, t.SM4, t.SM5, t.SM6, t.SM3_Tru, t.SM4_Tru, t.HT_Dat, t.HT_Khong_Dat,")
content = content.replace("for col in ['SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'SM6', 'SM4_Dat_HT', 'SM4_Khong_Dat_HT']:", "for col in ['SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'SM6', 'SM3_Tru', 'SM4_Tru', 'HT_Dat', 'HT_Khong_Dat']:")

with open("database.py", "w", encoding="utf-8") as f:
    f.write(content)

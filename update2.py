with open("database.py", "r", encoding="utf-8") as f:
    content = f.read()

target1 = """            SM6 REAL,
            PRIMARY KEY (Ngay_Bao_Cao, Ma_NV)
        )"""

replacement1 = """            SM6 REAL,
            SM3_Tru REAL,
            SM4_Tru REAL,
            HT_Dat REAL,
            HT_Khong_Dat REAL,
            PRIMARY KEY (Ngay_Bao_Cao, Ma_NV)
        )"""

content = content.replace(target1, replacement1)

target2 = """            cursor.execute('''
                INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM3, SM4)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                SM3=excluded.SM3, SM4=excluded.SM4
            ''', (date_str, ma_nv_extracted, ten_nv_extracted, to_ktdb, thang_du_lieu, sm3, sm4))"""

replacement2 = """            cursor.execute('''
                INSERT INTO kpi_daily (Ngay_Bao_Cao, Ma_NV, Ten_NV, To_KTDB, Thang_Du_Lieu, SM3, SM4, SM3_Tru, SM4_Tru, HT_Dat, HT_Khong_Dat)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(Ngay_Bao_Cao, Ma_NV) DO UPDATE SET
                Ten_NV=excluded.Ten_NV, To_KTDB=excluded.To_KTDB,
                SM3=excluded.SM3, SM4=excluded.SM4,
                SM3_Tru=excluded.SM3_Tru, SM4_Tru=excluded.SM4_Tru,
                HT_Dat=excluded.HT_Dat, HT_Khong_Dat=excluded.HT_Khong_Dat
            ''', (date_str, ma_nv_extracted, ten_nv_extracted, to_ktdb, thang_du_lieu, sm3, sm4, data['sm3_tru'], data['sm4_tru'], data['ht_dat'], data['ht_khong_dat']))"""

content = content.replace(target2, replacement2)

with open("database.py", "w", encoding="utf-8") as f:
    f.write(content)

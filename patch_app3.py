with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """            st.markdown("**Top 10 cá nhân có số lượng phiếu không đạt nhiều nhất**")
            valid_with_diff = valid_individuals.assign(So_Phieu_Khong_Dat=valid_individuals['SM4'] - valid_individuals['SM3'])
            worst_10 = valid_with_diff[valid_with_diff['So_Phieu_Khong_Dat'] > 0].sort_values('So_Phieu_Khong_Dat', ascending=False).head(10)
            worst_df = pd.DataFrame({
                'Nhân viên': worst_10['Ten_NV'] + ' (' + worst_10['To_KTDB'] + ')',
                'Số lượng phiếu không đạt': worst_10['So_Phieu_Khong_Dat']
            })"""

replacement = """            st.markdown("**Top 10 cá nhân có số lượng phiếu không đạt nhiều nhất**")
            valid_with_diff = valid_individuals.assign(
                So_Phieu_Khong_Dat=valid_individuals['SM4'] - valid_individuals['SM3'],
                Phieu_KDat_Loi_HT=valid_individuals['SM4'] - valid_individuals['SM4_Tru']
            )
            worst_10 = valid_with_diff[valid_with_diff['So_Phieu_Khong_Dat'] > 0].sort_values('So_Phieu_Khong_Dat', ascending=False).head(10)
            worst_df = pd.DataFrame({
                'Nhân viên': worst_10['Ten_NV'] + ' (' + worst_10['To_KTDB'] + ')',
                'Số lượng phiếu không đạt': worst_10['So_Phieu_Khong_Dat'].astype(int),
                'Số phiếu K.Đạt đã chuyển HT (đạt)': worst_10['Phieu_KDat_Loi_HT'].fillna(0).astype(int)
            })"""

content = content.replace(target, replacement)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

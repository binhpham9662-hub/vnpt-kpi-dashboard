with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """        brcd_agg = df.groupby('To_KTDB').agg(
            Tong_SM3=('SM3', 'sum'), Tong_SM4=('SM4', 'sum'),
            Tong_SM4_Dat_HT=('SM4_Dat_HT', 'sum'), Tong_SM4_Khong_Dat_HT=('SM4_Khong_Dat_HT', 'sum'),
            Tang_Khong_Dat_BRCD=('Tang_Khong_Dat_BRCD', 'sum')
        ).reset_index()
        
        brcd_agg['Tu_So'] = brcd_agg['Tong_SM3']
        brcd_agg['Mau_So'] = brcd_agg['Tong_SM4'] - brcd_agg['Tong_SM4_Dat_HT']
        brcd_agg['Ty_Le_Dat'] = (brcd_agg['Tu_So'] / brcd_agg['Mau_So'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Đơn vị': brcd_agg['To_KTDB'],
            'Chỉ tiêu': 'Tỷ lệ phiếu sửa chữa báo hỏng dịch vụ BRCĐ đúng quy định không tính hẹn',
            'SM3': brcd_agg['Tong_SM3'],
            'SM4': brcd_agg['Tong_SM4'],
            'SL phiếu đã chuyển HT đạt': brcd_agg['Tong_SM4_Dat_HT'],
            'SL phiếu đã chuyển HT không đạt': brcd_agg['Tong_SM4_Khong_Dat_HT'],
            'Số lượng phiếu không đạt': brcd_agg['Tong_SM4'] - brcd_agg['Tong_SM3'],
            'Số phiếu không đạt tăng lên so với hôm qua': brcd_agg['Tang_Khong_Dat_BRCD'].apply(lambda x: f"{x:+.0f}"),
            'Tỷ lệ đạt sau giảm trừ lỗi do hạ tầng': brcd_agg['Ty_Le_Dat'].apply(lambda x: f"{x:.2f}%")
        })"""

replacement = """        brcd_agg = df.groupby('To_KTDB').agg(
            Tong_SM3=('SM3', 'sum'), Tong_SM4=('SM4', 'sum'),
            Tong_SM3_Tru=('SM3_Tru', 'sum'), Tong_SM4_Tru=('SM4_Tru', 'sum'),
            Tong_HT_Dat=('HT_Dat', 'sum'), Tong_HT_Khong_Dat=('HT_Khong_Dat', 'sum'),
            Tang_Khong_Dat_BRCD=('Tang_Khong_Dat_BRCD', 'sum')
        ).reset_index()
        
        brcd_agg['Ty_Le_Dat_Truoc'] = (brcd_agg['Tong_SM3'] / brcd_agg['Tong_SM4'] * 100).fillna(0)
        brcd_agg['Ty_Le_Dat_Sau'] = (brcd_agg['Tong_SM3_Tru'] / brcd_agg['Tong_SM4_Tru'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Đơn vị': brcd_agg['To_KTDB'],
            'Chỉ tiêu': 'Tỷ lệ phiếu sửa chữa báo hỏng dịch vụ BRCĐ đúng quy định không tính hẹn',
            'SM3': brcd_agg['Tong_SM3'],
            'SM4': brcd_agg['Tong_SM4'],
            'SL phiếu đã chuyển HT đạt': brcd_agg['Tong_HT_Dat'],
            'SL phiếu đã chuyển HT không đạt': brcd_agg['Tong_HT_Khong_Dat'],
            'Số lượng phiếu không đạt': brcd_agg['Tong_SM4'] - brcd_agg['Tong_SM3'],
            'Số phiếu không đạt tăng lên so với hôm qua': brcd_agg['Tang_Khong_Dat_BRCD'].apply(lambda x: f"{x:+.0f}"),
            'Tỷ lệ trước giảm trừ': brcd_agg['Ty_Le_Dat_Truoc'].apply(lambda x: f"{x:.2f}%"),
            'Tỷ lệ đạt sau giảm trừ lỗi do hạ tầng': brcd_agg['Ty_Le_Dat_Sau'].apply(lambda x: f"{x:.2f}%")
        })"""

content = content.replace(target, replacement)

# also replace for team_df (render_individual_table)
target2 = """        team_df = valid_individuals[valid_individuals['To_KTDB'] == st.session_state.selected_team].copy()
        
        team_df['Mau_So'] = team_df['SM4'] - team_df['SM4_Dat_HT']
        team_df['Ty_Le_Dat'] = (team_df['SM3'] / team_df['Mau_So'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Nhân viên': team_df['Ten_NV'],
            'Mã NV': team_df['Ma_NV'],
            'Chỉ tiêu': 'C1.1 BRCĐ không tính hẹn',
            'SM3': team_df['SM3'],
            'SM4': team_df['SM4'],
            'SL phiếu đã chuyển HT đạt': team_df['SM4_Dat_HT'],
            'SL phiếu đã chuyển HT không đạt': team_df['SM4_Khong_Dat_HT'],
            'Phiếu không đạt': team_df['SM4'] - team_df['SM3'],
            'Tăng/giảm so với hôm qua': team_df['Tang_Khong_Dat_BRCD'].apply(lambda x: f"{x:+.0f}" if pd.notna(x) else "0"),
            'Tỷ lệ đạt sau giảm trừ lỗi do hạ tầng': team_df['Ty_Le_Dat'].apply(lambda x: f"{x:.2f}%")
        })"""

replacement2 = """        team_df = valid_individuals[valid_individuals['To_KTDB'] == st.session_state.selected_team].copy()
        
        team_df['Ty_Le_Dat_Truoc'] = (team_df['SM3'] / team_df['SM4'] * 100).fillna(0)
        team_df['Ty_Le_Dat_Sau'] = (team_df['SM3_Tru'] / team_df['SM4_Tru'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Nhân viên': team_df['Ten_NV'],
            'Mã NV': team_df['Ma_NV'],
            'Chỉ tiêu': 'C1.1 BRCĐ không tính hẹn',
            'SM3': team_df['SM3'],
            'SM4': team_df['SM4'],
            'SL phiếu đã chuyển HT đạt': team_df['HT_Dat'],
            'SL phiếu đã chuyển HT không đạt': team_df['HT_Khong_Dat'],
            'Phiếu không đạt': team_df['SM4'] - team_df['SM3'],
            'Tăng/giảm so với hôm qua': team_df['Tang_Khong_Dat_BRCD'].apply(lambda x: f"{x:+.0f}" if pd.notna(x) else "0"),
            'Tỷ lệ trước giảm trừ': team_df['Ty_Le_Dat_Truoc'].apply(lambda x: f"{x:.2f}%"),
            'Tỷ lệ đạt sau giảm trừ lỗi do hạ tầng': team_df['Ty_Le_Dat_Sau'].apply(lambda x: f"{x:.2f}%")
        })"""

content = content.replace(target2, replacement2)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

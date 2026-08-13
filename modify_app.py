with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_1 = '''    # Tính tổng Trung tâm
    total_center = summary_df['Total_Tickets'].sum()
    rows.append({
        "Hiển Thị": "🏢 Trung tâm Viễn thông Đông Anh",
        "Số Lượng Tồn": total_center,
        "_Level": "CENTER",
        "_Value": ""
    })'''

new_1 = '''    # Tính tổng Trung tâm
    total_center = summary_df['Total_Tickets'].sum()
    total_center_no_reason = int(summary_df['No_Reason_Tickets'].sum()) if 'No_Reason_Tickets' in summary_df.columns else 0
    rows.append({
        "Hiển Thị": "🏢 Trung tâm Viễn thông Đông Anh",
        "Số Lượng Tồn": total_center,
        "Chưa Có Lý Do": total_center_no_reason,
        "_Level": "CENTER",
        "_Value": ""
    })'''

old_2 = '''    # Nhóm theo Tổ
    for to_name, to_group in summary_df.groupby("To_KTDB"):
        total_to = to_group['Total_Tickets'].sum()
        rows.append({
            "Hiển Thị": f"   ├── 👥 {to_name}",
            "Số Lượng Tồn": total_to,
            "_Level": "TEAM",
            "_Value": to_name
        })'''

new_2 = '''    # Nhóm theo Tổ
    for to_name, to_group in summary_df.groupby("To_KTDB"):
        total_to = to_group['Total_Tickets'].sum()
        total_to_no_reason = int(to_group['No_Reason_Tickets'].sum()) if 'No_Reason_Tickets' in to_group.columns else 0
        rows.append({
            "Hiển Thị": f"   ├── 👥 {to_name}",
            "Số Lượng Tồn": total_to,
            "Chưa Có Lý Do": total_to_no_reason,
            "_Level": "TEAM",
            "_Value": to_name
        })'''

old_3 = '''        # Thêm Nhân Viên
        for _, row in to_group.iterrows():
            nv_name = row['NVKT']
            if isinstance(nv_name, str) and '-' in nv_name:
                nv_name = nv_name.split('-')[-1].strip()
            nv_tickets = row['Total_Tickets']
            rows.append({
                "Hiển Thị": f"   │    └── 👤 {nv_name}",
                "Số Lượng Tồn": nv_tickets,
                "_Level": "NVKT",
                "_Value": row['NVKT']
            })'''

new_3 = '''        # Thêm Nhân Viên
        for _, row in to_group.iterrows():
            nv_name = row['NVKT']
            if isinstance(nv_name, str) and '-' in nv_name:
                nv_name = nv_name.split('-')[-1].strip()
            nv_tickets = row['Total_Tickets']
            nv_no_reason = int(row['No_Reason_Tickets']) if 'No_Reason_Tickets' in row else 0
            rows.append({
                "Hiển Thị": f"   │    └── 👤 {nv_name}",
                "Số Lượng Tồn": nv_tickets,
                "Chưa Có Lý Do": nv_no_reason,
                "_Level": "NVKT",
                "_Value": row['NVKT']
            })'''

old_4 = '''    display_df = hierarchy_df[["Hiển Thị", qty_col_name]].copy()
    display_df.index = range(1, len(display_df) + 1)'''

new_4 = '''    display_cols = ["Hiển Thị", qty_col_name]
    if loai_phieu in ['PTTB', 'BHSC'] and 'Chưa Có Lý Do' in hierarchy_df.columns:
        display_cols.append('Chưa Có Lý Do')
    display_df = hierarchy_df[display_cols].copy()
    display_df.index = range(1, len(display_df) + 1)'''

content = content.replace(old_1, new_1)
content = content.replace(old_2, new_2)
content = content.replace(old_3, new_3)
content = content.replace(old_4, new_4)

with open(r'H:\web-bao-cao\app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done modifying app.py')

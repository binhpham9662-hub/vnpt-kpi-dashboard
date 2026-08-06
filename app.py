import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_kpi_for_date, init_db, get_pending_summary, get_pending_details
import os

# Initialize DB on first run if not exists
if not os.path.exists('kpi_history.db'):
    init_db()

st.set_page_config(
    page_title="HR KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    .stDataFrame {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    h1, h2, h3 {
        color: #1a252f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Make buttons look nicer */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session State initialization
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = None
if 'selected_metric' not in st.session_state:
    st.session_state.selected_metric = None

st.title("📊 Bảng Điều Khiển KPI Nhân Sự")
st.markdown("---")

# --- Cảnh báo trễ dữ liệu TOÀN CỤC ---
try:
    from database import get_kpi_for_date
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_df = get_kpi_for_date(today_str)
    if today_df.empty and datetime.now().hour >= 12:
        st.error(f"⚠️ **CẢNH BÁO:** Đã quá 12h00 trưa nhưng hệ thống chưa lấy được dữ liệu báo cáo của ngày hôm nay ({today_str}). Vui lòng mở Terminal và chạy lệnh `python scraper.py` để cập nhật số liệu mới nhất!")
except Exception:
    pass

with st.sidebar:
    st.header("📑 Điều hướng")
    is_main = st.session_state.page not in ['pending_bhsc', 'pending_pttb']
    if st.button("Trang chủ KPI", use_container_width=True, type="primary" if is_main else "secondary"):
        st.session_state.page = 'main'
        st.rerun()
    st.markdown("---")
    st.subheader("Báo Cáo Tồn")
    if st.button("Tồn Phiếu BHSC", use_container_width=True, type="primary" if st.session_state.page == 'pending_bhsc' else "secondary"):
        st.session_state.page = 'pending_bhsc'
        st.rerun()
    if st.button("Tồn Phiếu PTTB", use_container_width=True, type="primary" if st.session_state.page == 'pending_pttb' else "secondary"):
        st.session_state.page = 'pending_pttb'
        st.rerun()

# Date Selection
col_date, _ = st.columns([1, 4])
with col_date:
    selected_date = st.date_input("Chọn ngày xem báo cáo:", datetime.now())

date_str = selected_date.strftime("%Y-%m-%d")

# Fetch data from SQLite
try:
    df = get_kpi_for_date(date_str)
    # Đổi tên Tổ Không xác định thành Trung tâm Viễn thông Đông Anh
    if not df.empty:
        df['To_KTDB'] = df['To_KTDB'].replace('Không xác định', 'Trung tâm Viễn thông Đông Anh')
except Exception as e:
    st.error(f"Lỗi truy xuất cơ sở dữ liệu: {e}")
    st.stop()

if df.empty and st.session_state.page not in ['pending_bhsc', 'pending_pttb']:
    st.info(f"Chưa có dữ liệu KPI cho ngày {date_str}. Vui lòng kiểm tra lại quá trình tải dữ liệu hoặc chọn ngày khác.")
    st.stop()

def render_pending_tickets_page(loai_phieu):
    st.subheader(f"Bảng Tổng Hợp Phiếu Tồn {loai_phieu}")
    try:
        summary_df = get_pending_summary(date_str, loai_phieu)
    except Exception as e:
        st.error(f"Lỗi truy xuất dữ liệu phiếu tồn: {e}")
        return
        
    if summary_df.empty:
        st.info(f"Chưa có dữ liệu phiếu tồn {loai_phieu} cho ngày {date_str}.")
        return
        
    # Tạo bảng có index bắt đầu từ 1
    summary_df.index = range(1, len(summary_df) + 1)
    summary_df = summary_df.rename(columns={"To_KTDB": "Tổ KTĐB", "NVKT": "Nhân Viên KT", "Total_Tickets": "Số Lượng Tồn"})
    
    st.markdown("### 👥 Tổng hợp theo cá nhân")
    st.info("💡 **Mẹo:** Hãy tích vào ô vuông (checkbox) ở cột ngoài cùng bên trái của bảng để xem chi tiết phiếu tồn của nhân viên đó.")
    
    event = st.dataframe(summary_df, use_container_width=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        selected_idx = event.selection.rows[0]
        selected_nv = summary_df.iloc[selected_idx]['Nhân Viên KT']
        st.markdown("---")
        st.markdown(f"### 📋 Chi tiết phiếu tồn của: **{selected_nv}**")
        details_df = get_pending_details(date_str, loai_phieu, selected_nv)
        if details_df.empty:
            st.warning("Không có chi tiết.")
        else:
            details_df.index = range(1, len(details_df) + 1)
            st.dataframe(details_df, use_container_width=True)

def render_main_page():

    # --- Calculations ---
    total_sm1 = df['SM1'].sum()
    total_sm2 = df['SM2'].sum()
    total_sm3 = df['SM3'].sum()
    total_sm4 = df['SM4'].sum()
    if 'SM5' not in df.columns:
        df['SM5'] = 0
        df['SM6'] = 0
        df['Tang_Khong_Dat_BRCD_Lap'] = 0
    total_sm5 = df['SM5'].sum()
    total_sm6 = df['SM6'].sum()
    
    ty_le_brcd = (total_sm3 / total_sm4 * 100) if total_sm4 > 0 else 0
    ty_le_clcd = (total_sm1 / total_sm2 * 100) if total_sm2 > 0 else 0
    ty_le_brcd_lap = (total_sm5 / total_sm6 * 100) if total_sm6 > 0 else 0
    
    # Tính tỷ lệ các ngày trước
    y_ty_le_brcd = (df['Y_SM3'].sum() / df['Y_SM4'].sum() * 100) if df['Y_SM4'].sum() > 0 else 0
    d2_ty_le_brcd = (df['D2_SM3'].sum() / df['D2_SM4'].sum() * 100) if df['D2_SM4'].sum() > 0 else 0
    d3_ty_le_brcd = (df['D3_SM3'].sum() / df['D3_SM4'].sum() * 100) if df['D3_SM4'].sum() > 0 else 0
    d7_ty_le_brcd = (df['D7_SM3'].sum() / df['D7_SM4'].sum() * 100) if df['D7_SM4'].sum() > 0 else 0

    y_ty_le_clcd = (df['Y_SM1'].sum() / df['Y_SM2'].sum() * 100) if df['Y_SM2'].sum() > 0 else 0
    d2_ty_le_clcd = (df['D2_SM1'].sum() / df['D2_SM2'].sum() * 100) if df['D2_SM2'].sum() > 0 else 0
    d3_ty_le_clcd = (df['D3_SM1'].sum() / df['D3_SM2'].sum() * 100) if df['D3_SM2'].sum() > 0 else 0
    d7_ty_le_clcd = (df['D7_SM1'].sum() / df['D7_SM2'].sum() * 100) if df['D7_SM2'].sum() > 0 else 0

    y_ty_le_brcd_lap = (df['Y_SM5'].sum() / df['Y_SM6'].sum() * 100) if df['Y_SM6'].sum() > 0 else 0
    d2_ty_le_brcd_lap = (df['D2_SM5'].sum() / df['D2_SM6'].sum() * 100) if df['D2_SM6'].sum() > 0 else 0
    d3_ty_le_brcd_lap = (df['D3_SM5'].sum() / df['D3_SM6'].sum() * 100) if df['D3_SM6'].sum() > 0 else 0
    d7_ty_le_brcd_lap = (df['D7_SM5'].sum() / df['D7_SM6'].sum() * 100) if df['D7_SM6'].sum() > 0 else 0

    st.subheader("📌 Tổng Quan KPI")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric(
            label="C1.1 BRCĐ không tính hẹn", 
            value=f"{ty_le_brcd:.2f}%", 
            delta="Mục tiêu: ≥ 85%",
            delta_color="normal" if ty_le_brcd >= 85 else "inverse"
        )
        st.caption(f"🕒 1 ngày trước: **{y_ty_le_brcd:.2f}%**<br>🕒 2 ngày trước: **{d2_ty_le_brcd:.2f}%**<br>🕒 3 ngày trước: **{d3_ty_le_brcd:.2f}%**<br>🕒 7 ngày trước: **{d7_ty_le_brcd:.2f}%**", unsafe_allow_html=True)
        if st.button("👁 Xem bảng BRCĐ", use_container_width=True):
            st.session_state.page = 'table_brcd'
            st.rerun()
            
    with m2:
        st.metric(
            label="C1.2 BRCĐ lặp lại", 
            value=f"{ty_le_brcd_lap:.2f}%", 
            delta="Mục tiêu: ≤ 2.5%",
            delta_color="inverse" if ty_le_brcd_lap > 2.5 else "normal"
        )
        st.caption(f"🕒 1 ngày trước: **{y_ty_le_brcd_lap:.2f}%**<br>🕒 2 ngày trước: **{d2_ty_le_brcd_lap:.2f}%**<br>🕒 3 ngày trước: **{d3_ty_le_brcd_lap:.2f}%**<br>🕒 7 ngày trước: **{d7_ty_le_brcd_lap:.2f}%**", unsafe_allow_html=True)
        if st.button("👁 Xem bảng BRCĐ Lặp", use_container_width=True):
            st.session_state.page = 'table_brcd_lap'
            st.rerun()
            
    with m3:
        st.metric(
            label="C1.1 CLCĐ FiberVNN, MyTV", 
            value=f"{ty_le_clcd:.2f}%", 
            delta="Mục tiêu: ≥ 99%",
            delta_color="normal" if ty_le_clcd >= 99 else "inverse"
        )
        st.caption(f"🕒 1 ngày trước: **{y_ty_le_clcd:.2f}%**<br>🕒 2 ngày trước: **{d2_ty_le_clcd:.2f}%**<br>🕒 3 ngày trước: **{d3_ty_le_clcd:.2f}%**<br>🕒 7 ngày trước: **{d7_ty_le_clcd:.2f}%**", unsafe_allow_html=True)
        if st.button("👁 Xem bảng CLCĐ", use_container_width=True):
            st.session_state.page = 'table_clcd'
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📉 Xem Biểu Đồ Phân Tích", use_container_width=True, type="primary"):
        st.session_state.page = 'charts'
        st.rerun()

def render_team_table(metric_type):
    st.button("⬅ Quay lại Tổng quan", on_click=lambda: st.session_state.update(page='main'))
    
    st.info("💡 **Mẹo:** Hãy nhấp vào bất kỳ hàng nào trong bảng để xem chi tiết từng nhân sự của Tổ đó.")
    
    if metric_type == 'brcd':
        st.subheader("📊 Bảng Chỉ tiêu C1.1 BRCĐ không tính hẹn")
        brcd_agg = df.groupby('To_KTDB').agg(
            Tong_SM3=('SM3', 'sum'), Tong_SM4=('SM4', 'sum'),
            Tang_Khong_Dat_BRCD=('Tang_Khong_Dat_BRCD', 'sum')
        ).reset_index()
        brcd_agg['Ty_Le_Dat'] = (brcd_agg['Tong_SM3'] / brcd_agg['Tong_SM4'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Đơn vị': brcd_agg['To_KTDB'],
            'Chỉ tiêu': 'Tỷ lệ phiếu sửa chữa báo hỏng dịch vụ BRCĐ đúng quy định không tính hẹn',
            'SM3': brcd_agg['Tong_SM3'],
            'SM4': brcd_agg['Tong_SM4'],
            'Số phiếu không đạt tăng lên so với hôm qua': brcd_agg['Tang_Khong_Dat_BRCD'].apply(lambda x: f"{x:+.0f}"),
            'Tỷ lệ đạt': brcd_agg['Ty_Le_Dat'].apply(lambda x: f"{x:.2f}%")
        })
    elif metric_type == 'brcd_lap':
        st.subheader("📊 Bảng Chỉ tiêu C1.2 BRCĐ lặp lại")
        brcd_lap_agg = df.groupby('To_KTDB').agg(
            Tong_SM5=('SM5', 'sum'), Tong_SM6=('SM6', 'sum'),
            Tang_Khong_Dat_BRCD_Lap=('Tang_Khong_Dat_BRCD_Lap', 'sum')
        ).reset_index()
        brcd_lap_agg['Ty_Le_Dat'] = (brcd_lap_agg['Tong_SM5'] / brcd_lap_agg['Tong_SM6'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Đơn vị': brcd_lap_agg['To_KTDB'],
            'Chỉ tiêu': 'Tỷ lệ thuê bao báo hỏng dịch vụ BRCĐ lặp lại',
            'SM1': brcd_lap_agg['Tong_SM5'],
            'SM2': brcd_lap_agg['Tong_SM6'],
            'Số phiếu lặp tăng lên so với hôm qua': brcd_lap_agg['Tang_Khong_Dat_BRCD_Lap'].apply(lambda x: f"{x:+.0f}"),
            'Tỷ lệ lặp': brcd_lap_agg['Ty_Le_Dat'].apply(lambda x: f"{x:.2f}%")
        })
    else:
        st.subheader("📊 Bảng Chỉ tiêu C1.1 CLCĐ FiberVNN, MyTV")
        clcd_agg = df.groupby('To_KTDB').agg(
            Tong_SM1=('SM1', 'sum'), Tong_SM2=('SM2', 'sum'),
            Tang_Khong_Dat_CLCD=('Tang_Khong_Dat_CLCD', 'sum')
        ).reset_index()
        clcd_agg['Ty_Le_Dat'] = (clcd_agg['Tong_SM1'] / clcd_agg['Tong_SM2'] * 100).fillna(0)
        
        display_df = pd.DataFrame({
            'Đơn vị': clcd_agg['To_KTDB'],
            'Chỉ tiêu': 'Tỷ lệ sửa chữa phiếu chất lượng chủ động dịch vụ FiberVNN, MyTV đạt yêu cầu',
            'SM1': clcd_agg['Tong_SM1'],
            'SM2': clcd_agg['Tong_SM2'],
            'Số phiếu không đạt tăng lên so với hôm qua': clcd_agg['Tang_Khong_Dat_CLCD'].apply(lambda x: f"{x:+.0f}"),
            'Tỷ lệ đạt': clcd_agg['Ty_Le_Dat'].apply(lambda x: f"{x:.2f}%")
        })
        
    display_df.index = range(1, len(display_df) + 1)
    
    event = st.dataframe(display_df, use_container_width=True, selection_mode="single-row", on_select="rerun")
    
    if event.selection.rows:
        selected_idx = event.selection.rows[0]
        st.session_state.selected_team = display_df.iloc[selected_idx]['Đơn vị']
        st.session_state.selected_metric = metric_type
        st.session_state.page = 'team_detail'
        st.rerun()
        
    st.markdown("---")
    st.subheader("⚠️ Cảnh báo cá nhân cần lưu ý (Toàn mạng)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valid_individuals = df[(df['Ten_NV'].str.strip() != '') & (~df['Ma_NV'].str.contains('(?i)trung tâm|đông anh', na=False))]
        
        if metric_type == 'brcd':
            st.markdown("**Top 5 cá nhân có Tỷ lệ thấp nhất**")
            worst_5 = valid_individuals[valid_individuals['SM4'] > 0].sort_values('Ty_Le_BRCD', ascending=True).head(5)
            worst_df = pd.DataFrame({
                'Nhân viên': worst_5['Ten_NV'] + ' (' + worst_5['To_KTDB'] + ')',
                'Tỷ lệ': worst_5['Ty_Le_BRCD'].apply(lambda x: f"{x*100:.2f}%")
            })
            st.dataframe(worst_df, use_container_width=True, hide_index=True)
        elif metric_type == 'clcd':
            st.markdown("**Top 5 cá nhân có Tỷ lệ thấp nhất**")
            worst_5 = valid_individuals[valid_individuals['SM2'] > 0].sort_values('Ty_Le_CLCD', ascending=True).head(5)
            worst_df = pd.DataFrame({
                'Nhân viên': worst_5['Ten_NV'] + ' (' + worst_5['To_KTDB'] + ')',
                'Tỷ lệ': worst_5['Ty_Le_CLCD'].apply(lambda x: f"{x*100:.2f}%")
            })
            st.dataframe(worst_df, use_container_width=True, hide_index=True)
        elif metric_type == 'brcd_lap':
            st.markdown("**Top 5 cá nhân có số lượng hỏng lặp nhiều nhất**")
            worst_5 = valid_individuals[valid_individuals['SM5'] > 0].sort_values('SM5', ascending=False).head(5)
            worst_df = pd.DataFrame({
                'Nhân viên': worst_5['Ten_NV'] + ' (' + worst_5['To_KTDB'] + ')',
                'Số lượng': worst_5['SM5'].astype(int)
            })
            st.dataframe(worst_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Top 3 cá nhân có số phiếu tăng đột biến**")
        
        if metric_type == 'brcd':
            st.markdown("*So với 1 ngày trước*")
            top_3_inc = valid_individuals.sort_values('Tang_Khong_Dat_BRCD', ascending=False).head(3)
            inc_df = pd.DataFrame({
                'Nhân viên': top_3_inc['Ten_NV'] + ' (' + top_3_inc['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc['Tang_Khong_Dat_BRCD'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df, use_container_width=True, hide_index=True)
            
            st.markdown("*So với 2 ngày trước*")
            top_3_inc_2d = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_2d', ascending=False).head(3)
            inc_df_2d = pd.DataFrame({
                'Nhân viên': top_3_inc_2d['Ten_NV'] + ' (' + top_3_inc_2d['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc_2d['Tang_Khong_Dat_BRCD_2d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_2d, use_container_width=True, hide_index=True)
            st.markdown("*So với 3 ngày trước*")
            top_3_inc_3d = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_3d', ascending=False).head(3)
            inc_df_3d = pd.DataFrame({
                'Nhân viên': top_3_inc_3d['Ten_NV'] + ' (' + top_3_inc_3d['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc_3d['Tang_Khong_Dat_BRCD_3d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_3d, use_container_width=True, hide_index=True)
            
            st.markdown("*So với 7 ngày trước*")
            top_3_inc_7d = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_7d', ascending=False).head(3)
            inc_df_7d = pd.DataFrame({
                'Nhân viên': top_3_inc_7d['Ten_NV'] + ' (' + top_3_inc_7d['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc_7d['Tang_Khong_Dat_BRCD_7d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_7d, use_container_width=True, hide_index=True)

        elif metric_type == 'clcd':
            st.markdown("*So với 1 ngày trước*")
            top_3_inc = valid_individuals.sort_values('Tang_Khong_Dat_CLCD', ascending=False).head(3)
            inc_df = pd.DataFrame({
                'Nhân viên': top_3_inc['Ten_NV'] + ' (' + top_3_inc['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc['Tang_Khong_Dat_CLCD'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df, use_container_width=True, hide_index=True)
            
            st.markdown("*So với 2 ngày trước*")
            top_3_inc_2d = valid_individuals.sort_values('Tang_Khong_Dat_CLCD_2d', ascending=False).head(3)
            inc_df_2d = pd.DataFrame({
                'Nhân viên': top_3_inc_2d['Ten_NV'] + ' (' + top_3_inc_2d['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc_2d['Tang_Khong_Dat_CLCD_2d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_2d, use_container_width=True, hide_index=True)
            st.markdown("*So với 3 ngày trước*")
            top_3_inc_3d = valid_individuals.sort_values('Tang_Khong_Dat_CLCD_3d', ascending=False).head(3)
            inc_df_3d = pd.DataFrame({
                'Nhân viên': top_3_inc_3d['Ten_NV'] + ' (' + top_3_inc_3d['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc_3d['Tang_Khong_Dat_CLCD_3d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_3d, use_container_width=True, hide_index=True)
            
            st.markdown("*So với 7 ngày trước*")
            top_3_inc_7d = valid_individuals.sort_values('Tang_Khong_Dat_CLCD_7d', ascending=False).head(3)
            inc_df_7d = pd.DataFrame({
                'Nhân viên': top_3_inc_7d['Ten_NV'] + ' (' + top_3_inc_7d['To_KTDB'] + ')',
                'Phiếu tăng': top_3_inc_7d['Tang_Khong_Dat_CLCD_7d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_7d, use_container_width=True, hide_index=True)

        elif metric_type == 'brcd_lap':
            st.markdown("*So với 1 ngày trước*")
            top_3_inc = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_Lap', ascending=False).head(3)
            inc_df = pd.DataFrame({
                'Nhân viên': top_3_inc['Ten_NV'] + ' (' + top_3_inc['To_KTDB'] + ')',
                'Phiếu lặp tăng': top_3_inc['Tang_Khong_Dat_BRCD_Lap'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df, use_container_width=True, hide_index=True)
            
            st.markdown("*So với 2 ngày trước*")
            top_3_inc_2d = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_Lap_2d', ascending=False).head(3)
            inc_df_2d = pd.DataFrame({
                'Nhân viên': top_3_inc_2d['Ten_NV'] + ' (' + top_3_inc_2d['To_KTDB'] + ')',
                'Phiếu lặp tăng': top_3_inc_2d['Tang_Khong_Dat_BRCD_Lap_2d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_2d, use_container_width=True, hide_index=True)
            st.markdown("*So với 3 ngày trước*")
            top_3_inc_3d = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_Lap_3d', ascending=False).head(3)
            inc_df_3d = pd.DataFrame({
                'Nhân viên': top_3_inc_3d['Ten_NV'] + ' (' + top_3_inc_3d['To_KTDB'] + ')',
                'Phiếu lặp tăng': top_3_inc_3d['Tang_Khong_Dat_BRCD_Lap_3d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_3d, use_container_width=True, hide_index=True)
            
            st.markdown("*So với 7 ngày trước*")
            top_3_inc_7d = valid_individuals.sort_values('Tang_Khong_Dat_BRCD_Lap_7d', ascending=False).head(3)
            inc_df_7d = pd.DataFrame({
                'Nhân viên': top_3_inc_7d['Ten_NV'] + ' (' + top_3_inc_7d['To_KTDB'] + ')',
                'Phiếu lặp tăng': top_3_inc_7d['Tang_Khong_Dat_BRCD_Lap_7d'].apply(lambda x: f"+{x:.0f}" if pd.notna(x) and x > 0 else f"{x:.0f}")
            })
            st.dataframe(inc_df_7d, use_container_width=True, hide_index=True)

def render_team_detail():
    st.button("⬅ Quay lại Bảng Tổ", on_click=lambda: st.session_state.update(page=f"table_{st.session_state.selected_metric}"))
    team_name = st.session_state.selected_team
    st.subheader(f"🏢 Chi tiết nhân sự: {team_name}")
    
    team_df = df[df['To_KTDB'] == team_name].copy()
    
    # Format Đơn vị column combining Ma_NV and Ten_NV
    team_df['Đơn vị'] = team_df['Ma_NV'] + " - " + team_df['Ten_NV']
    
    if st.session_state.selected_metric == 'brcd':
        display_df = pd.DataFrame({
            'Đơn vị': team_df['Đơn vị'],
            'SM3': team_df['SM3'],
            'SM4': team_df['SM4'],
            'Số phiếu không đạt tăng lên so với hôm qua': team_df['Tang_Khong_Dat_BRCD'].apply(lambda x: f"=(SM4-SM3)hôm nay - (SM4-SM3)hôm qua" if pd.isna(x) else f"{x:+.0f}"),
            'Tỷ lệ phiếu sửa chữa báo hỏng dịch vụ BRCĐ đúng quy định không tính hẹn': team_df['Ty_Le_BRCD'].apply(lambda x: f"{x*100:.2f}%")
        })
    elif st.session_state.selected_metric == 'brcd_lap':
        display_df = pd.DataFrame({
            'Đơn vị': team_df['Đơn vị'],
            'SM1': team_df['SM5'],
            'SM2': team_df['SM6'],
            'Số phiếu lặp tăng lên so với hôm qua': team_df['Tang_Khong_Dat_BRCD_Lap'].apply(lambda x: f"=(SM1)hôm nay - (SM1)hôm qua" if pd.isna(x) else f"{x:+.0f}"),
            'Tỷ lệ thuê bao báo hỏng dịch vụ BRCĐ lặp lại': team_df['Ty_Le_BRCD_Lap'].apply(lambda x: f"{x*100:.2f}%")
        })
    else:
        display_df = pd.DataFrame({
            'Đơn vị': team_df['Đơn vị'],
            'SM1': team_df['SM1'],
            'SM2': team_df['SM2'],
            'Số phiếu không đạt tăng lên so với hôm qua': team_df['Tang_Khong_Dat_CLCD'].apply(lambda x: f"=(SM2-SM1)hôm nay - (SM2-SM1)hôm qua" if pd.isna(x) else f"{x:+.0f}"),
            'Tỷ lệ sửa chữa phiếu chất lượng chủ động dịch vụ FiberVNN, MyTV đạt yêu cầu': team_df['Ty_Le_CLCD'].apply(lambda x: f"{x*100:.2f}%")
        })

    display_df.index = range(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True)

def render_charts_page():
    st.button("⬅ Quay lại Tổng quan", on_click=lambda: st.session_state.update(page='main'))
    st.subheader("📉 Biểu Đồ Phân Tích Xu Hướng")
    
    import sqlite3
    import os
    DB_PATH = os.path.join(os.path.dirname(__file__), 'kpi_history.db')
    
    conn = sqlite3.connect(DB_PATH)
    months_df = pd.read_sql_query("SELECT DISTINCT Thang_Du_Lieu FROM kpi_daily ORDER BY Thang_Du_Lieu DESC", conn)
    months_list = months_df['Thang_Du_Lieu'].tolist()
    
    if not months_list:
        st.info("Chưa có dữ liệu lịch sử để hiển thị biểu đồ.")
        conn.close()
        return
        
    selected_month = st.selectbox("📅 Chọn Chu Kỳ Báo Cáo (Tính từ ngày 26 tháng trước đến ngày 25 tháng này):", months_list)
    
    query = "SELECT * FROM kpi_daily WHERE Thang_Du_Lieu = ?"
    hist_df = pd.read_sql_query(query, conn, params=(selected_month,))
    conn.close()
    
    if hist_df.empty:
        st.warning("Không có dữ liệu trong khoảng thời gian này.")
        return
        
    hist_df['To_KTDB'] = hist_df['To_KTDB'].replace('Không xác định', 'Trung tâm Viễn thông Đông Anh')
    
    import altair as alt
    
    # --- 1. Trung tâm Viễn thông Đông Anh ---
    st.markdown("---")
    st.markdown("### 🏢 Trung tâm Viễn thông Đông Anh")
    st.info("Xu hướng Tỷ lệ Đạt theo Ngày của toàn Trung tâm")
    
    tt_df = hist_df[hist_df['To_KTDB'] == 'Trung tâm Viễn thông Đông Anh'].copy()
    if not tt_df.empty:
        tt_daily = tt_df.groupby('Ngay_Bao_Cao').agg(
            Tong_SM1=('SM1', 'sum'), Tong_SM2=('SM2', 'sum'),
            Tong_SM3=('SM3', 'sum'), Tong_SM4=('SM4', 'sum'),
            Tong_SM5=('SM5', 'sum'), Tong_SM6=('SM6', 'sum')
        ).reset_index()
        tt_daily['Ngay_Bao_Cao'] = pd.to_datetime(tt_daily['Ngay_Bao_Cao'])
        
        tt_daily['brcd'] = (tt_daily['Tong_SM3'] / tt_daily['Tong_SM4'] * 100).fillna(0)
        tt_daily['brcd_lap'] = (tt_daily['Tong_SM5'] / tt_daily['Tong_SM6'] * 100).fillna(0)
        tt_daily['clcd'] = (tt_daily['Tong_SM1'] / tt_daily['Tong_SM2'] * 100).fillna(0)
        
        def render_single_chart(df, y_col, color, title):
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X('Ngay_Bao_Cao:T', title='Ngày', axis=alt.Axis(format='%Y-%m-%d', labelAngle=-45)),
                y=alt.Y(f'{y_col}:Q', scale=alt.Scale(zero=False), title=title),
                color=alt.value(color),
                tooltip=[alt.Tooltip('Ngay_Bao_Cao:T', format='%Y-%m-%d', title='Ngày'), alt.Tooltip(f'{y_col}:Q', format='.2f', title=title)]
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        
        st.markdown("**1. C1.1 BRCĐ không tính hẹn**")
        render_single_chart(tt_daily, 'brcd', '#1f77b4', 'C1.1 BRCĐ không tính hẹn (%)')
        
        st.markdown("**2. C1.2 BRCĐ lặp lại**")
        render_single_chart(tt_daily, 'brcd_lap', '#ff7f0e', 'C1.2 BRCĐ lặp lại (%)')
        
        st.markdown("**3. C1.1 CLCĐ FiberVNN, MyTV**")
        render_single_chart(tt_daily, 'clcd', '#2ca02c', 'C1.1 CLCĐ FiberVNN, MyTV (%)')
    else:
        st.warning("Không có dữ liệu của Trung tâm.")

    # --- 2. Các Tổ Viễn thông ---
    st.markdown("---")
    st.markdown("### 👷 So sánh các Tổ Kỹ thuật địa bàn")
    st.info("So sánh xu hướng giữa các Tổ viễn thông. Mỗi đường biểu diễn một Tổ.")
    
    to_df = hist_df[hist_df['To_KTDB'] != 'Trung tâm Viễn thông Đông Anh'].copy()
    if not to_df.empty:
        to_daily = to_df.groupby(['Ngay_Bao_Cao', 'To_KTDB']).agg(
            Tong_SM1=('SM1', 'sum'), Tong_SM2=('SM2', 'sum'),
            Tong_SM3=('SM3', 'sum'), Tong_SM4=('SM4', 'sum'),
            Tong_SM5=('SM5', 'sum'), Tong_SM6=('SM6', 'sum')
        ).reset_index()
        to_daily['Ngay_Bao_Cao'] = pd.to_datetime(to_daily['Ngay_Bao_Cao'])
        
        to_daily['brcd'] = (to_daily['Tong_SM3'] / to_daily['Tong_SM4'] * 100).fillna(0)
        to_daily['brcd_lap'] = (to_daily['Tong_SM5'] / to_daily['Tong_SM6'] * 100).fillna(0)
        to_daily['clcd'] = (to_daily['Tong_SM1'] / to_daily['Tong_SM2'] * 100).fillna(0)
        
        def render_multi_chart(df, y_col, title):
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X('Ngay_Bao_Cao:T', title='Ngày', axis=alt.Axis(format='%Y-%m-%d', labelAngle=-45)),
                y=alt.Y(f'{y_col}:Q', scale=alt.Scale(zero=False), title=title),
                color=alt.Color('To_KTDB:N', legend=alt.Legend(title="Tổ", orient="bottom")),
                tooltip=[alt.Tooltip('Ngay_Bao_Cao:T', format='%Y-%m-%d', title='Ngày'), alt.Tooltip('To_KTDB:N', title='Tổ'), alt.Tooltip(f'{y_col}:Q', format='.2f', title=title)]
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        
        st.markdown("**1. C1.1 BRCĐ không tính hẹn**")
        render_multi_chart(to_daily, 'brcd', 'C1.1 BRCĐ không tính hẹn (%)')
        
        st.markdown("**2. C1.2 BRCĐ lặp lại**")
        render_multi_chart(to_daily, 'brcd_lap', 'C1.2 BRCĐ lặp lại (%)')
        
        st.markdown("**3. C1.1 CLCĐ FiberVNN, MyTV**")
        render_multi_chart(to_daily, 'clcd', 'C1.1 CLCĐ FiberVNN, MyTV (%)')
    else:
        st.warning("Không có dữ liệu của các Tổ.")


# Main Routing
if st.session_state.page == 'main':
    render_main_page()
elif st.session_state.page == 'table_brcd':
    render_team_table('brcd')
elif st.session_state.page == 'table_brcd_lap':
    render_team_table('brcd_lap')
elif st.session_state.page == 'table_clcd':
    render_team_table('clcd')
elif st.session_state.page == 'team_detail':
    render_team_detail()
elif st.session_state.page == 'charts':
    render_charts_page()
elif st.session_state.page == 'pending_bhsc':
    render_pending_tickets_page('BHSC')
elif st.session_state.page == 'pending_pttb':
    render_pending_tickets_page('PTTB')

st.markdown("---")
st.caption("Thiết kế và phát triển dựa trên Streamlit & Pandas. Tự động lấy dữ liệu bằng Playwright.")
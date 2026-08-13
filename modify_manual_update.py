with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_section = '''    st.markdown("---")
    st.subheader("🔄 Cập nhật thủ công")
    st.info("Nút này sẽ gửi tín hiệu xuống Máy Tính Cá Nhân để tự động bật trình duyệt và lấy báo cáo.")
    
    if st.button("🚀 Lấy Báo Cáo Tổng Quan KPI", use_container_width=True):
        try:
            import requests
            requests.post("https://ntfy.sh/vnpt_scraper_trigger_b8f2d9a74c1e9x3q", data="RUN_KPI".encode(encoding='utf-8'))
            st.toast("✅ Đã gửi lệnh chạy lấy Báo Cáo KPI xuống máy tính!")
        except Exception as e:
            st.error(f"Lỗi gửi lệnh: {e}")
            
    if st.button("🚀 Lấy Báo Cáo Chi Tiết Hỏng Lặp", use_container_width=True):
        try:
            import requests
            requests.post("https://ntfy.sh/vnpt_scraper_trigger_b8f2d9a74c1e9x3q", data="RUN_SM1".encode(encoding='utf-8'))
            st.toast("✅ Đã gửi lệnh lấy Báo cáo Hỏng Lặp xuống máy tính!")
        except Exception as e:
            st.error(f"Lỗi gửi lệnh: {e}")'''

new_section = '''    if st.session_state.current_user == "binhpt5":
        st.markdown("---")
        st.subheader("🔄 Cập nhật thủ công")
        st.info("Nút này sẽ gửi tín hiệu xuống Máy Tính Cá Nhân để tự động bật trình duyệt và lấy báo cáo.")
        
        if st.button("🚀 Lấy Báo Cáo Tổng Quan KPI", use_container_width=True):
            try:
                import requests
                requests.post("https://ntfy.sh/vnpt_scraper_trigger_b8f2d9a74c1e9x3q", data="RUN_KPI".encode(encoding='utf-8'))
                st.toast("✅ Đã gửi lệnh chạy lấy Báo Cáo KPI xuống máy tính!")
            except Exception as e:
                st.error(f"Lỗi gửi lệnh: {e}")
                
        if st.button("🚀 Lấy Báo Cáo Chi Tiết Hỏng Lặp", use_container_width=True):
            try:
                import requests
                requests.post("https://ntfy.sh/vnpt_scraper_trigger_b8f2d9a74c1e9x3q", data="RUN_SM1".encode(encoding='utf-8'))
                st.toast("✅ Đã gửi lệnh lấy Báo cáo Hỏng Lặp xuống máy tính!")
            except Exception as e:
                st.error(f"Lỗi gửi lệnh: {e}")'''

content = content.replace(old_section, new_section)
with open(r'H:\web-bao-cao\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

import sys

with open(r'H:\web-bao-cao\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

login_code = '''
# --- Bắt đầu tính năng Đăng nhập ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.authenticated:
    st.title("🔒 Đăng nhập hệ thống Báo cáo")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập")
            
            if submit:
                valid_users = {
                    "binhpt5": "Binh#1991",
                    "ngoctb": "Trungtam@5",
                    "dungtt.hni": "Trungtam@5",
                    "anhdv1": "Trungtam@5",
                    "sonpq.hni": "Trungtam@5",
                    "haonx.hni": "Trungtam@5",
                    "huyhung.hni": "Trungtam@5",
                    "thont.hni": "Trungtam@5"
                }
                if username in valid_users and valid_users[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không chính xác.")
    st.stop()
# --- Kết thúc tính năng Đăng nhập ---

'''

# Insert after CSS block
insert_pos = content.find('# Session State initialization')
if insert_pos != -1:
    new_content = content[:insert_pos] + login_code + content[insert_pos:]
    with open(r'H:\web-bao-cao\app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected login code successfully!")
else:
    print("Could not find '# Session State initialization' in app.py")

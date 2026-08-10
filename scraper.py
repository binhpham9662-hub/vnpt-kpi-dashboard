import time
import os
from datetime import datetime
import schedule
from playwright.sync_api import sync_playwright
import telebot
import requests
import json
import logging
from database import process_and_insert_excel, save_pending_tickets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = "8685247292:AAEsGy0S2JT0ek0yQyiDesp3rTTQeCKv6mQ"
CHAT_ID = "763228783"

# Dùng telebot chỉ để GỬI tin nhắn (không gọi getUpdates/polling để tránh xung đột 409)
bot = telebot.TeleBot(TOKEN)

def get_otp_from_ntfy(timeout=180):
    """
    Hứng OTP tự động từ ntfy.sh (nơi app Android gửi lên) để tránh xung đột Telegram.
    """
    ntfy_url = "https://ntfy.sh/vnpt_otp_secret_b8f2d9a74c1e9x3q/json?poll=1"
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            resp = requests.get(ntfy_url, timeout=5)
            if resp.status_code == 200:
                lines = resp.text.strip().split('\n')
                if lines and lines[-1]:
                    last_msg = json.loads(lines[-1])
                    msg_time = last_msg.get("time", 0)
                    # Bỏ qua tin nhắn cũ (đã có từ trước khi script chạy)
                    if msg_time >= start_time - 10:
                        if "message" in last_msg:
                            text = str(last_msg["message"]).strip()
                            # Lọc tìm 6 chữ số
                            import re
                            match = re.search(r'\d{6}', text)
                            if match:
                                return match.group(0)
        except Exception as e:
            pass
        time.sleep(3)
    return None

def perform_scraping():
    logging.info("Bắt đầu quá trình scraping...")
    
    with sync_playwright() as p:
        # Sử dụng Microsoft Edge theo yêu cầu của user và mở full màn hình
        browser = p.chromium.launch(headless=False, channel="msedge", args=['--start-maximized'])
        context = browser.new_context(accept_downloads=True, no_viewport=True)
        
        # Tạm thời tắt tính năng lưu cookies (auth.json) để ép bot luôn phải đăng nhập lại mỗi khi test
        # state_file = 'auth.json'
        # if os.path.exists(state_file):
        #     context = browser.new_context(storage_state=state_file, accept_downloads=True, no_viewport=True)
            
        page = context.new_page()
        
        target_url = "https://baocao.hanoi.vnpt.vn/report/report-info?id=534964&menu_id=535020"
        page.goto(target_url, timeout=60000)
        
        # --- BƯỚC 1: ĐIỀN TÀI KHOẢN ---
        try:
            page.wait_for_selector("input[placeholder='Tên đăng nhập']", timeout=5000)
            needs_login = True
        except:
            needs_login = False
            
        if needs_login:
            logging.info("Yêu cầu đăng nhập...")
            page.get_by_placeholder("Tên đăng nhập").fill("binhpt5")
            page.get_by_placeholder("Mật khẩu").fill("Binh#1991")
            
            # Bấm ĐĂNG NHẬP để web VNPT bắn tin nhắn SMS về máy sếp
            page.get_by_role("button", name="ĐĂNG NHẬP").click()
            
            # --- BƯỚC 2: CHỜ MÀN HÌNH OTP VÀ NHẬP OTP ---
            logging.info("Hệ thống yêu cầu OTP. Đang chờ lấy OTP từ ntfy.sh (từ app Android)...")
            try:
                bot.send_message(CHAT_ID, "Hệ thống đang chờ OTP từ Android qua kênh ntfy...")
            except:
                pass
            
            current_otp = get_otp_from_ntfy(180)
            if not current_otp:
                logging.error("Không nhận được OTP, dừng tiến trình báo cáo.")
                browser.close()
                return
            
            logging.info(f"Đã nhận OTP: {current_otp}")
            try:
                bot.send_message(CHAT_ID, f"Đã nhận OTP tự động: {current_otp}. Đang tiếp tục...")
            except:
                pass
                
            try:
                page.wait_for_timeout(2000) # Đợi giao diện OTP trồi lên
                
                # Quét tìm ô chữ nhật trên màn hình để điền 6 số OTP vào
                page.locator("input:visible").first.fill(current_otp)
                
                # Bấm xác nhận OTP
                page.get_by_role("button", name="ĐĂNG NHẬP").click()
            except Exception as e:
                logging.error(f"Chưa tìm thấy ô nhập OTP, lỗi: {e}")
                browser.close()
                return
                
            page.wait_for_load_state("networkidle") # Đợi mạng lắng xuống (load web xong)
            page.wait_for_timeout(2000)
            
            # context.storage_state(path=state_file)
            # logging.info("Đã lưu cookies đăng nhập.")
            
        # VNPT hay có lỗi là đăng nhập xong nó đá về trang chủ, ta phải cưỡng chế vào lại đúng link báo cáo
        page.goto(target_url, timeout=60000)
        page.wait_for_load_state("networkidle")
        
        logging.info("Đang thiết lập thông số báo cáo...")
        page.wait_for_timeout(3000)
        
        # --- BƯỚC 3: CHỌN CÁC Ô TÙY CHỌN TRÊN WEB ---
        # Mở dropdown "Đơn vị" (dropdown đầu tiên - sử dụng ngx-dropdown-treeview)
        try:
            page.locator('ngx-dropdown-treeview button.dropdown-toggle').first.click(timeout=5000)
            page.wait_for_timeout(1000)
            
            # Chỉ tìm ô input bên trong ngx-dropdown-treeview
            page.locator("ngx-dropdown-treeview input[placeholder='Tìm kiếm']").first.fill("TTVT Đông Anh")
            page.wait_for_timeout(1000)
                
            # Click bằng get_by_text (khớp một phần, bỏ qua khoảng trắng thừa)
            page.get_by_text("TTVT Đông Anh", exact=False).last.click()
            page.keyboard.press("Escape")
        except Exception as e:
            logging.error(f"Lỗi khi chọn Đơn vị: {e}")
            
        page.wait_for_timeout(1000)
        
        # Chọn "Loại" (sử dụng ng-select, đang hiển thị là Khu vực quản lý)
        try:
            # Click vào ng-select có chứa text Khu vực quản lý
            page.locator('ng-select').filter(has_text='Khu vực quản lý').first.click(timeout=5000)
            page.wait_for_timeout(1000)
            
            # Click bằng get_by_text để chắc chắn khớp dù có khoảng trắng hay viết hoa/thường
            page.get_by_text("NVKT quản lý địa bàn", exact=False).last.click()
            page.keyboard.press("Escape")
        except Exception as e:
            logging.error(f"Lỗi khi chọn Loại: {e}")
            
        page.wait_for_timeout(1000)
        
        try:
            page.locator("button:has-text('Báo cáo'), a:has-text('Báo cáo')").locator("visible=true").first.click()
            logging.info("Đã bấm Báo cáo. Đang chờ dữ liệu...")
            page.wait_for_timeout(10000)
        except:
            pass

        logging.info("Bắt đầu xuất Excel...")
        try:
            # Tìm nút Xuất Excel hiển thị trên màn hình
            btn_xuat_excel = page.locator("button:has-text('Xuất Excel'), a:has-text('Xuất Excel'), span:has-text('Xuất Excel')").locator("visible=true").first
            btn_xuat_excel.wait_for(state="visible", timeout=30000)
            btn_xuat_excel.click()
            logging.info("Đã bấm Xuất Excel C1.1, đang đợi menu xổ xuống...")
            
            page.wait_for_timeout(2000)
            
            btn_tat_ca = page.get_by_text("Tất cả dữ liệu", exact=False).locator("visible=true").last
            btn_tat_ca.wait_for(state="visible", timeout=15000)
            with page.expect_download(timeout=60000) as download_info:
                btn_tat_ca.click()
                
            download = download_info.value
            downloads_dir = "downloads"
            os.makedirs(downloads_dir, exist_ok=True)
            
            file_name = f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = os.path.join(downloads_dir, file_name)
            download.save_as(file_path)
            logging.info(f"Đã tải file Excel: {file_path}")
            
            if process_and_insert_excel(file_path):
                try:
                    bot.send_message(CHAT_ID, "✅ Đã tải và cập nhật dữ liệu KPI thành công vào Database.")
                except:
                    pass
            else:
                try:
                    bot.send_message(CHAT_ID, "❌ Có lỗi trong quá trình xử lý file Excel.")
                except:
                    pass
                
        except Exception as e:
            logging.error(f"Lỗi khi xuất/tải Excel: {e}")
            try:
                bot.send_message(CHAT_ID, f"❌ Lỗi khi xuất Excel: {str(e)}")
            except:
                pass

        # --- BÁO CÁO C1.2 ---
        try:
            logging.info("Chuyển sang link báo cáo C1.2...")
            target_url_2 = "https://baocao.hanoi.vnpt.vn/report/report-info?id=522513&menu_id=535021"
            page.goto(target_url_2, timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            
            # Mở dropdown "Đơn vị"
            page.locator('ngx-dropdown-treeview button.dropdown-toggle').first.click(timeout=5000)
            page.wait_for_timeout(1000)
            page.locator("ngx-dropdown-treeview input[placeholder='Tìm kiếm']").first.fill("TTVT Đông Anh")
            page.wait_for_timeout(1000)
            page.get_by_text("TTVT Đông Anh", exact=False).last.click()
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            
            # Chọn "Loại"
            page.locator('ng-select').filter(has_text='Khu vực quản lý').first.click(timeout=5000)
            page.wait_for_timeout(1000)
            page.get_by_text("NVKT quản lý địa bàn", exact=False).last.click()
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            
            page.locator("button:has-text('Báo cáo'), a:has-text('Báo cáo')").locator("visible=true").first.click()
            logging.info("Đã bấm Báo cáo C1.2. Đang chờ dữ liệu...")
            
            # Đợi lâu hơn một chút để báo cáo load xong
            page.wait_for_timeout(10000)
            
            # Tìm nút Xuất Excel hiển thị trên màn hình
            btn_xuat_excel = page.locator("button:has-text('Xuất Excel'), a:has-text('Xuất Excel'), span:has-text('Xuất Excel')").locator("visible=true").first
            btn_xuat_excel.wait_for(state="visible", timeout=30000)
            btn_xuat_excel.click()
            logging.info("Đã bấm Xuất Excel C1.2, đang đợi menu xổ xuống...")
            
            page.wait_for_timeout(2000)
            
            btn_tat_ca = page.get_by_text("Tất cả dữ liệu", exact=False).locator("visible=true").last
            btn_tat_ca.wait_for(state="visible", timeout=15000)
            with page.expect_download(timeout=60000) as download_info2:
                btn_tat_ca.click()
                
            download2 = download_info2.value
            file_name2 = f"kpi_report_C1_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path2 = os.path.join(downloads_dir, file_name2)
            download2.save_as(file_path2)
            logging.info(f"Đã tải file Excel C1.2: {file_path2}")
            
            if process_and_insert_excel(file_path2, report_type="C1.2"):
                try:
                    bot.send_message(CHAT_ID, "✅ Đã tải và cập nhật dữ liệu KPI C1.2 thành công vào Database.")
                except:
                    pass
            else:
                try:
                    bot.send_message(CHAT_ID, "❌ Có lỗi trong quá trình xử lý file Excel C1.2.")
                except:
                    pass
                    
        except Exception as e:
            logging.error(f"Lỗi khi xuất/tải Excel C1.2: {e}")
            try:
                bot.send_message(CHAT_ID, f"❌ Lỗi khi xuất Excel C1.2: {str(e)}")
            except:
                pass

        browser.close()

def job():
    logging.info("Chạy tác vụ tự động...")
    try:
        perform_scraping()
        
        # Tự động đẩy DB lên GitHub sau khi cào thành công
        import subprocess
        bat_path = os.path.join(os.path.dirname(__file__), "sync_to_web.bat")
        if os.path.exists(bat_path):
            logging.info("Bắt đầu đồng bộ dữ liệu lên Web (GitHub)...")
            try:
                subprocess.run([bat_path], check=True, shell=True)
                logging.info("Đồng bộ lên Web thành công!")
            except Exception as e:
                logging.error(f"Lỗi khi đồng bộ lên Web: {e}")
                
    except Exception as e:
        logging.error(f"Lỗi hệ thống: {e}")

def sync_overdue_bhsc():
    logging.info("Bắt đầu đồng bộ phiếu tồn BHSC...")
    file_path = r"H:\vnpt_report\daily_overdue.json"
    if not os.path.exists(file_path):
        logging.error(f"Không tìm thấy file {file_path}")
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data: return
        today_str = datetime.now().strftime('%Y-%m-%d')
        if today_str in data:
            target_date = today_str
        else:
            target_date = list(data.keys())[-1]
            
        save_pending_tickets(target_date, "BHSC", data[target_date])
        logging.info(f"Đã đồng bộ phiếu tồn BHSC cho ngày {target_date}")
    except Exception as e:
        logging.error(f"Lỗi khi đồng bộ BHSC: {e}")

def sync_overdue_pttb():
    logging.info("Bắt đầu đồng bộ phiếu tồn PTTB...")
    file_path = r"H:\vnpt_report\daily_overdue_pttb.json"
    if not os.path.exists(file_path):
        logging.error(f"Không tìm thấy file {file_path}")
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data: return
        today_str = datetime.now().strftime('%Y-%m-%d')
        if today_str in data:
            target_date = today_str
        else:
            target_date = list(data.keys())[-1]
            
        save_pending_tickets(target_date, "PTTB", data[target_date])
        logging.info(f"Đã đồng bộ phiếu tồn PTTB cho ngày {target_date}")
    except Exception as e:
        logging.error(f"Lỗi khi đồng bộ PTTB: {e}")

def get_report_dates():
    today = datetime.now()
    if today.day > 25:
        end_month = (today.month % 12) + 1
        end_year = today.year + (1 if today.month == 12 else 0)
        start_month = today.month
        start_year = today.year
    else:
        end_month = today.month
        end_year = today.year
        start_month = 12 if today.month == 1 else today.month - 1
        start_year = today.year - (1 if today.month == 1 else 0)
        
    start_date_str = f"26/{start_month:02d}/{start_year}"
    end_date_str = f"25/{end_month:02d}/{end_year}"
    return start_date_str, end_date_str

def run_download_sm1():
    import glob
    import os
    import re
    DOWNLOAD_DIR = "downloads"
    logging.info("Dọn dẹp file SM1 cũ...")
    for f in glob.glob(os.path.join(DOWNLOAD_DIR, "SM1_C12_*.xlsx")):
        try:
            os.remove(f)
        except:
            pass
            
    logging.info("Bắt đầu quá trình tải báo cáo SM1 C12 2026...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge", args=['--start-maximized'])
        context = browser.new_context(accept_downloads=True, no_viewport=True)
        page = context.new_page()
        
        target_url = "https://baocao.hanoi.vnpt.vn/report/report-info?id=267215&menu_id=276194"
        page.goto(target_url, timeout=60000)
        
        try:
            page.wait_for_selector("input[placeholder='Tên đăng nhập']", timeout=5000)
            needs_login = True
        except:
            needs_login = False
            
        if needs_login:
            logging.info("Yêu cầu đăng nhập...")
            page.get_by_placeholder("Tên đăng nhập").fill("binhpt5")
            page.get_by_placeholder("Mật khẩu").fill("Binh#1991")
            page.get_by_role("button", name="ĐĂNG NHẬP").click()
            
            logging.info("Hệ thống yêu cầu OTP. Đang chờ lấy OTP từ ntfy.sh...")
            try: bot.send_message(CHAT_ID, "Hệ thống SM1 C12 đang chờ OTP...")
            except: pass
            
            current_otp = get_otp_from_ntfy(180)
            if not current_otp:
                logging.error("Không nhận được OTP, dừng tiến trình báo cáo.")
                browser.close()
                return
            
            logging.info(f"Đã nhận OTP: {current_otp}")
            try:
                page.wait_for_timeout(2000)
                page.locator("input:visible").first.fill(current_otp)
                page.get_by_role("button", name="ĐĂNG NHẬP").click()
            except Exception as e:
                logging.error(f"Lỗi nhập OTP: {e}")
                browser.close()
                return
                
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            
        page.goto(target_url, timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        
        logging.info("Chọn Đơn vị...")
        try:
            page.locator('ngx-dropdown-treeview button.dropdown-toggle').first.click(timeout=5000)
            page.wait_for_timeout(1000)
            page.locator("ngx-dropdown-treeview input[placeholder='Tìm kiếm']").first.fill("TTVT Đông Anh")
            page.wait_for_timeout(1000)
            page.get_by_text("TTVT Đông Anh", exact=False).last.click()
            page.keyboard.press("Escape")
        except Exception as e:
            logging.error(f"Lỗi khi chọn Đơn vị: {e}")
            
        page.wait_for_timeout(1000)

        start_date, end_date = get_report_dates()
        logging.info(f"Chọn ngày: {start_date} đến {end_date}")
        try:
            inputs = page.locator("input.mat-datepicker-input")
            if inputs.count() >= 2:
                inputs.nth(0).click(timeout=5000, force=True)
                page.wait_for_timeout(1000)
                inputs.nth(0).click(timeout=5000, force=True)
                page.wait_for_timeout(500)
                page.keyboard.press("Control+A")
                page.keyboard.type(start_date)
                
                page.wait_for_timeout(500)
                page.keyboard.press("Escape")
                page.mouse.click(10, 10)
                page.wait_for_timeout(1000)
            else:
                logging.warning("Không tìm thấy đủ 2 ô nhập ngày mat-datepicker-input")
        except Exception as e:
            logging.error(f"Lỗi nhập ngày: {e}")

        page.wait_for_timeout(1000)

        logging.info("Chọn Loại phiếu...")
        try:
            dropdown = page.locator('ng-select').filter(has_text='HTTT').first
            dropdown.click(timeout=5000)
            page.wait_for_timeout(1000)
            
            page.keyboard.type("SM1 C12 2026")
            page.wait_for_timeout(1000)
            
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
        except Exception as e:
            logging.error(f"Lỗi chọn Loại phiếu: {e}")

        page.wait_for_timeout(1000)

        try:
            page.locator("button:has-text('Báo cáo'), a:has-text('Báo cáo')").locator("visible=true").first.click()
            logging.info("Đã bấm Báo cáo. Đang chờ dữ liệu load (khoảng 10s)...")
            page.wait_for_timeout(10000)
        except Exception as e:
            logging.error(f"Lỗi khi bấm nút Báo cáo: {e}")

        logging.info("Bắt đầu tải Excel...")
        try:
            btn_xuat_excel = page.locator("button:has-text('Xuất Excel'), a:has-text('Xuất Excel'), span:has-text('Xuất Excel')").locator("visible=true").first
            btn_xuat_excel.wait_for(state="visible", timeout=30000)
            btn_xuat_excel.click()
            logging.info("Đã bấm Xuất Excel, đợi menu...")
            
            page.wait_for_timeout(2000)
            
            btn_tat_ca = page.get_by_text("Tất cả dữ liệu", exact=False).locator("visible=true").last
            btn_tat_ca.wait_for(state="visible", timeout=15000)
            
            with page.expect_download(timeout=90000) as download_info:
                btn_tat_ca.click()
                
            download = download_info.value
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            
            file_name = f"SM1_C12_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = os.path.join(DOWNLOAD_DIR, file_name)
            download.save_as(file_path)
            logging.info(f"✅ Đã tải thành công file Excel: {file_path}")
            
            try: bot.send_message(CHAT_ID, f"✅ Đã tải thành công báo cáo SM1 C12 2026: {file_name}")
            except: pass
            
            from database import process_repeated_tickets_excel
            from datetime import timedelta
            yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            process_repeated_tickets_excel(file_path, yesterday_str)
            
            # Đẩy lên Web ngay sau khi lấy xong
            import subprocess
            bat_path = os.path.join(os.path.dirname(__file__), "sync_to_web.bat")
            if os.path.exists(bat_path):
                subprocess.run([bat_path], check=True, shell=True)
                
        except Exception as e:
            logging.error(f"Lỗi tải Excel: {e}")
            try: bot.send_message(CHAT_ID, f"❌ Lỗi tải Excel SM1 C12: {str(e)}")
            except: pass

        browser.close()

def listen_for_triggers():
    import threading
    import queue
    import json
    
    task_queue = queue.Queue()
    
    def worker():
        while True:
            msg = task_queue.get()
            if msg == "RUN_KPI":
                logging.info("Thực thi lấy Báo cáo KPI theo yêu cầu từ Web...")
                try:
                    perform_scraping()
                    import subprocess
                    bat_path = os.path.join(os.path.dirname(__file__), "sync_to_web.bat")
                    if os.path.exists(bat_path):
                        subprocess.run([bat_path], check=True, shell=True)
                except Exception as e:
                    logging.error(f"Lỗi khi chạy KPI: {e}")
            elif msg == "RUN_SM1":
                logging.info("Thực thi lấy Báo cáo Hỏng Lặp SM1 theo yêu cầu từ Web...")
                try:
                    run_download_sm1()
                except Exception as e:
                    logging.error(f"Lỗi khi chạy SM1: {e}")
            task_queue.task_done()
            
    threading.Thread(target=worker, daemon=True).start()
    
    def listener():
        logging.info("Bắt đầu luồng nghe tín hiệu từ Web qua ntfy.sh (topic: vnpt_scraper_trigger_b8f2d9a74c1e9x3q)...")
        while True:
            try:
                resp = requests.get("https://ntfy.sh/vnpt_scraper_trigger_b8f2d9a74c1e9x3q/json", stream=True, timeout=60)
                for line in resp.iter_lines():
                    if line:
                        data = json.loads(line)
                        if data.get('event') == 'message':
                            msg = data.get('message', '').strip()
                            logging.info(f"Nhận được tín hiệu từ Web: {msg}")
                            if msg in ["RUN_KPI", "RUN_SM1"]:
                                task_queue.put(msg)
            except Exception as e:
                logging.error(f"Lỗi kết nối ntfy listener: {e}")
                time.sleep(5)
    
    threading.Thread(target=listener, daemon=True).start()

if __name__ == "__main__":
    from database import init_db
    init_db()
    
    # Lắng nghe tín hiệu từ Web
    listen_for_triggers()
    
    # Sửa lịch báo cáo sang 8:00
    schedule.every().day.at("08:00").do(job)
    schedule.every().day.at("08:05").do(sync_overdue_bhsc)
    schedule.every().day.at("08:10").do(sync_overdue_pttb)
    schedule.every().day.at("08:15").do(run_download_sm1)
    
    logging.info("Hệ thống đã khởi động.")
    # Tạm thời tắt tự chạy khi khởi động để tránh spam
    # job()
    # sync_overdue_bhsc()
    # sync_overdue_pttb()
    
    while True:
        schedule.run_pending()
        time.sleep(10)

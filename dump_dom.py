import time
from playwright.sync_api import sync_playwright

def dump():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge", args=['--start-maximized'])
        context = browser.new_context(accept_downloads=True, no_viewport=True)
        page = context.new_page()
        
        target_url = "https://baocao.hanoi.vnpt.vn/report/report-info?id=544180&menu_id=544229"
        page.goto(target_url, timeout=60000)
        
        try:
            page.wait_for_selector("input[placeholder='Tên đăng nhập']", timeout=5000)
            page.get_by_placeholder("Tên đăng nhập").fill("binhpt5")
            page.get_by_placeholder("Mật khẩu").fill("Binh#1991")
            page.get_by_role("button", name="ĐĂNG NHẬP").click()
            print("Vui lòng nhập OTP vào trình duyệt và bấm ĐĂNG NHẬP (bạn có 60 giây)...")
            time.sleep(60) # Wait for manual OTP entry
        except:
            pass
            
        page.goto(target_url, timeout=60000)
        page.wait_for_load_state("networkidle")
        time.sleep(10)
        
        with open("dom_dump.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("Đã lưu dom_dump.html")
        browser.close()

if __name__ == "__main__":
    dump()

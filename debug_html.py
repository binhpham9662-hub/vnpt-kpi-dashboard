import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="msedge")
    state_file = 'auth.json'
    if os.path.exists(state_file):
        context = browser.new_context(storage_state=state_file, accept_downloads=True)
    else:
        context = browser.new_context(accept_downloads=True)
        
    page = context.new_page()
    target_url = "https://baocao.hanoi.vnpt.vn/report/report-info?id=534964&menu_id=535020"
    page.goto(target_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print("Saved page_source.html")
    browser.close()

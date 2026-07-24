import sqlite3
import datetime
import telebot
import os

TOKEN = "8685247292:AAEsGy0S2JT0ek0yQyiDesp3rTTQeCKv6mQ"
CHAT_ID = "763228783"

DB_PATH = os.path.join(os.path.dirname(__file__), 'kpi_history.db')

def check_and_alert():
    # Kiểm tra xem có file DB không
    if not os.path.exists(DB_PATH):
        print("Không tìm thấy Database.")
        return

    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM kpi_daily WHERE Ngay_Bao_Cao = ?', (today_str,))
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        bot = telebot.TeleBot(TOKEN)
        msg = f"⚠️ CẢNH BÁO: Đã 12h00 trưa nhưng hệ thống chưa lấy được dữ liệu báo cáo của ngày hôm nay ({today_str}). Vui lòng mở máy và chạy Bot để lấy số liệu!"
        try:
            bot.send_message(CHAT_ID, msg)
            print("Đã gửi cảnh báo Telegram thành công.")
        except Exception as e:
            print(f"Lỗi gửi Telegram: {e}")
    else:
        print(f"Ngày {today_str} đã có dữ liệu. Không cần cảnh báo.")

if __name__ == "__main__":
    check_and_alert()

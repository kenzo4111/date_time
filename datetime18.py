import telebot
from datetime import datetime, timedelta
import time
import threading

# Bot tokenini o'rnating
bot = telebot.TeleBot("7833832466:AAHW1C9tTZGEna5tZkCUnT-1HwIOzBImyMc")  # Tokenni almashtiring

# Guruhlar va foydalanuvchilar ma'lumotlari
groups = {
    -1002382726672: {"users": [6406104865, 1517027489], "alert_1": "Salom", "alert_2": "Jarima sizga!"},  # Guruh 1
#    -1002492269472: {"users": [6406104865, 1517027489], "alert_1": "Nima gap", "alert_2": "Ogohlantiraman!"},  # Guruh 2
}

# Oxirgi xabar yuborilgan vaqtni har bir guruh uchun saqlash
last_message_times = {group_id: None for group_id in groups.keys()}
alert_1_sent = {group_id: False for group_id in groups.keys()}
alert_2_sent = {group_id: False for group_id in groups.keys()}

# Faoliyat kuzatish vaqt oralig'i
monitor_start_hour = 13
monitor_start_minute = 38
monitor_end_hour = 13
monitor_end_minute = 39

# Xabar yuborilmaganida javob vaqtlarini sozlash
alert_hour_1 = 13
alert_minute_1 = 40
alert_hour_2 = 13
alert_minute_2 = 41

# Foydalanuvchi xabar yuborganini aniqlash
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'sticker', 'video_note'])
def track_user_activity(message):
    global last_message_times, alert_1_sent, alert_2_sent
    if message.chat.id in groups:
        if message.from_user.id in groups[message.chat.id]["users"]:
            last_message_times[message.chat.id] = datetime.now()
            # Ogohlantirish holatini qayta tiklash
            alert_1_sent[message.chat.id] = False
            alert_2_sent[message.chat.id] = False
            print(f"Foydalanuvchi {message.from_user.id} guruh {message.chat.id} da xabar yubordi: {last_message_times[message.chat.id]}")

# Faoliyatni kuzatish
def monitor_user_activity():
    global last_message_times, alert_1_sent, alert_2_sent
    while True:
        now = datetime.now()
        start_time = now.replace(hour=monitor_start_hour, minute=monitor_start_minute, second=0, microsecond=0)
        end_time = now.replace(hour=monitor_end_hour, minute=monitor_end_minute, second=0, microsecond=0)
        alert_time_1 = now.replace(hour=alert_hour_1, minute=alert_minute_1, second=0, microsecond=0)
        alert_time_2 = now.replace(hour=alert_hour_2, minute=alert_minute_2, second=0, microsecond=0)

        for group_id, group_data in groups.items():
            if start_time <= now <= end_time:
                if last_message_times[group_id] is None or last_message_times[group_id] < start_time:
                    print(f"Guruh {group_id} uchun foydalanuvchilar {start_time} va {end_time} orasida xabar yubormadi.")

            # Birinchi ogohlantirish
            if now >= alert_time_1 and not alert_1_sent[group_id] and (last_message_times[group_id] is None or last_message_times[group_id] < start_time):
                bot.send_message(group_id, group_data["alert_1"])
                alert_1_sent[group_id] = True
                print(f"Guruh {group_id} uchun birinchi ogohlantirish yuborildi.")

            # Ikkinchi ogohlantirish
            if now >= alert_time_2 and not alert_2_sent[group_id] and (last_message_times[group_id] is None or last_message_times[group_id] < start_time):
                bot.send_message(group_id, group_data["alert_2"])
                alert_2_sent[group_id] = True
                print(f"Guruh {group_id} uchun ikkinchi ogohlantirish yuborildi.")

        time.sleep(10)  # Resurslarni tejash uchun oraliq vaqtni sozlash

# Foydalanuvchini kuzatishni boshlash
monitor_thread = threading.Thread(target=monitor_user_activity, daemon=True)
monitor_thread.start()

# Botni ishga tushirish
print("Bot ishlashni boshladi...")
bot.polling(none_stop=True)

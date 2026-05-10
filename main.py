from pyrogram import Client, filters
import time

# Твої дані
API_ID = 39835391
API_HASH = "c5731d2a4b90069d97e79d5e0e9423dc"

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

# Налаштування часу (у секундах)
OFFLINE_THRESHOLD = 600  # 10 хвилин твоєї відсутності
IGNORE_TIME = 300  # 5 хвилин паузи для одного чату

# Пам'ять бота
last_replied_users = {}
last_active_time = 0


@app.on_message(filters.me)
async def track_my_activity(client, message):
    global last_active_time
    last_active_time = time.time()
    print("✅ Твоя активність зафіксована. Таймер 10 хв скинуто.")


@app.on_message(filters.private & ~filters.me)
async def auto_reply(client, message):
    global last_active_time
    user_id = message.from_user.id
    current_time = time.time()

    # 1. Перевірка твоєї активності (чи минуло 10 хв)
    time_since_active = current_time - last_active_time
    if last_active_time != 0 and time_since_active < OFFLINE_THRESHOLD:
        return

    # 2. Перевірка анти-флуду (чи минуло 5 хв для цієї людини)
    last_reply_to_this_user = last_replied_users.get(user_id, 0)

    if (current_time - last_reply_to_this_user) > IGNORE_TIME:
        print(f"📩 Надсилаю авто-відповідь для {user_id}")

        # Твій новий текст
        await message.reply_text("😘Я ЗАРАЗ НЕ ОНЛАЙН БУДУ В СИТИ ОТВЕЧУ ЦЕ АВТО АТВЕЧИК😘")

        # Оновлюємо час відповіді
        last_replied_users[user_id] = current_time
    else:
        print(f"⏳ Пауза 5 хв ще триває для {user_id}. Бот мовчить.")


if __name__ == "__main__":
    print("🚀 Бот запущений!")
    print("Текст: 😘Я ЗАРАЗ НЕ ОНЛАЙН БУДУ В СИТИ ОТВЕЧУ ЦЕ АВТО АТВЕЧИК😘")
    app.run()
from telegram import Update, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Установи переменную окружения на Render
ADMIN_IDS = [1336840991, 5037239323]
DB_PATH = "users.db"

# Создание таблицы
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balance INTEGER DEFAULT 0,
    last_active TEXT
)
""")
conn.commit()

# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    now = datetime.datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, last_active) VALUES (?, ?, ?)",
                   (user.id, user.username, now))
    conn.commit()

    greeting = f"Привет, {user.first_name}!\nДобро пожаловать в рулетку ✨"
    keyboard = [[KeyboardButton("▶ Играть")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(chat_id=chat_id, text=greeting, reply_markup=markup)

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()  # Оставляем polling, если Render как background worker

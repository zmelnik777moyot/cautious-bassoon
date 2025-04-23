# Админ ID
ADMIN_IDS = [1336840991, 5037239323]

# Токен бота
BOT_TOKEN = "8089851764:AAEbJmSeFb8lY1LbHJLqMy9c6ZVpY8gWw_g"

# WebApp ссылка
WEBAPP_URL = "https://zmelnik77moyot.github.io/cautious-bassoon/"

from telegram import Update, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import datetime

# Путь к базе данных
DB_PATH = "users.db"

# Подключение и создание таблицы
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    stars INTEGER DEFAULT 0,
    last_active TEXT
)
""")
conn.commit()

# Регистрация или обновление пользователя
def register_user(user):
    user_id = user.id
    username = user.username or ""
    now = datetime.datetime.now().isoformat()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, username, last_active) VALUES (?, ?, ?)",
            (user_id, username, now)
        )
    else:
        cursor.execute(
            "UPDATE users SET last_active = ? WHERE user_id = ?",
            (now, user_id)
        )
    conn.commit()

# Обработка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    register_user(user)

    greeting_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"🌟 Добро пожаловать в звёздную игру!\n"
        f"🎲 Жми кнопку ниже, чтобы открыть игру:"
    )

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton(text="🚀 Играть!", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=greeting_text,
        reply_markup=reply_markup
    )

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

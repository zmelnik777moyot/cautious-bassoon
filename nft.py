### config.py

BOT_TOKEN = "8089851764:AAEbJmSeFb8lY1LbHJLqMy9c6ZVpY8gWw_g"
WEBHOOK_URL = "https://zmelnik777moyot.github.io/cautious-bassoon/"
ADMINS = [123456789, 987654321]  # список Telegram ID админов


### db.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///users.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)

Base.metadata.create_all(engine)

def get_all_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users


### bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from config import BOT_TOKEN, ADMINS
from db import get_all_users

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start_cmd(message: Message):
    await message.answer("\U0001F680 Добро пожаловать в Рулетку на звезды! \n\nПопробуй удачу и выигрывай звезды. Используй /spin, чтобы крутить рулетку!")

@dp.message(commands=["users"])
async def users_cmd(message: Message):
    if message.from_user.id in ADMINS:
        users = get_all_users()
        if not users:
            await message.answer("База пуста.")
        else:
            text = "\n".join(f"{u.id} - @{u.username or 'нет ника'}" for u in users)
            await message.answer(f"Пользователи:\n{text}")
    else:
        await message.answer("У тебя нет доступа.")


### main.py

from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.dispatcher.webhook import WebhookRequestHandler
from bot import dp, bot
from config import WEBHOOK_URL

app = FastAPI()
handler = WebhookRequestHandler(dispatcher=dp)

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@app.post("/webhook")
async def telegram_webhook(req: Request):
    return await handler.handle(req)

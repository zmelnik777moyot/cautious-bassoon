### config.py

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN, ADMINS
from db import get_all_users

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "\U0001F680 Добро пожаловать в Рулетку на звезды! \n\n"
        "Попробуй удачу и выигрывай звезды. Используй /spin, чтобы крутить рулетку!",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="🚀 Перейти в миниапп",
                    web_app=types.WebAppInfo(url="https://zmelnik777moyot.github.io/cautious-bassoon/")
                )]
            ]
        )
    )

@dp.message(Command("users"))
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

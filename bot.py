from aiogram import types, F, Router
from aiogram.filters import Command
from config import ADMINS
from db import get_all_users

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🚀 Добро пожаловать в рулетку!")

@router.message(Command("users"))
async def users_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        users = get_all_users()
        if not users:
            await message.answer("База пуста.")
        else:
            text = "\n".join(f"{u.id} - @{u.username or 'нет ника'}" for u in users)
            await message.answer(f"Пользователи:\n{text}")
    else:
        await message.answer("У тебя нет доступа.")

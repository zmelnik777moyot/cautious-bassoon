from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from config import BOT_TOKEN, WEBHOOK_URL
from bot import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp._process_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "ok", "message": "бот работает"}

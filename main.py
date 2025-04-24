from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from config import BOT_TOKEN, WEBHOOK_URL
import os
import uvicorn

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
@app.get("/")
async def root():
    return {"status": "ok", "message": "Рулетка живёт 🌟"}

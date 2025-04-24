from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.dispatcher.webhook import WebhookRequestHandler
from bot import dp, bot
from config import WEBHOOK_URL
import os
import uvicorn

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

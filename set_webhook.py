import requests

# Вставь сюда свой токен бота и адрес сайта:
BOT_TOKEN = "8089851764:AAEbJmSeFb8lY1LbHJLqMy9c6ZVpY8gWw_g"
WEBHOOK_URL = "https://cautious-bassoon-1.onrender.com/webhook"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": WEBHOOK_URL}

response = requests.post(url, data=payload)

print("\nСтатус установки вебхука:", response.status_code)
print("Ответ Telegram:", response.json())

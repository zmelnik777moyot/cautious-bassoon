import requests

BOT_TOKEN = "8089851764:AAEbJmSeFb8lY1LbHJLqMy9c6ZVpY8gWw_g"
WEBHOOK_URL = "https://zmelnik777moyot.github.io/cautious-bassoon/"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": WEBHOOK_URL}

response = requests.post(url, data=payload)

print("Статус установки вебхука:", response.status_code)
print("Ответ Telegram:", response.json())

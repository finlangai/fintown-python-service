from app.utils import time
import requests, os


def send(message: str):
    embed = {
        "embeds": [
            {
                "title": "Python Service",
                "description": message,
                "color": 3534184,
                "footer": {
                    "text": "Fintown",
                    "icon_url": "https://firebasestorage.googleapis.com/v0/b/fintown-4ddd6.appspot.com/o/logo%2Ffintown-logo.png?alt=media",
                },
                "timestamp": time.iso_now(),
            }
        ]
    }
    return requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json=embed)

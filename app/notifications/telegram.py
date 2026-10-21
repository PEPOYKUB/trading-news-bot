import httpx
from .base import NotificationProvider
class TelegramNotification(NotificationProvider):
    def __init__(self, token: str, chat_id: str): self.token, self.chat_id = token, chat_id
    def send(self, message: str) -> bool:
        if not self.token or not self.chat_id: return False
        response = httpx.post(f"https://api.telegram.org/bot{self.token}/sendMessage", data={"chat_id": self.chat_id, "text": message}, timeout=15)
        response.raise_for_status(); return True

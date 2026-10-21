from .base import NotificationProvider
class ConsoleNotification(NotificationProvider):
    def send(self, message: str) -> bool:
        print(f"[NOTIFICATION] {message}"); return True

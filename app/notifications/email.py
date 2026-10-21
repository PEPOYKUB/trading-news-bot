from .base import NotificationProvider
class EmailNotification(NotificationProvider):
    def send(self, message: str) -> bool:
        raise NotImplementedError("Configure SMTP credentials and an approved sender before enabling email")

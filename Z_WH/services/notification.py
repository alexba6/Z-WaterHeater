from .mail import MailManager
from email.message import EmailMessage


class NotificationManagerError(Exception):
    def __init__(self, message: str):
        self.message = message


class Notification:
    def __init__(self):
        self.subject: str = ''
        self.content: str = ''
        self.email: str = ''

    def getEmail(self) -> EmailMessage:
        mail = EmailMessage()
        mail['From'] = 'Z-WaterHeater'
        mail['Subject'] = self.subject
        mail['To'] = self.email
        mail.set_content(self.content)
        return mail


class NotificationManager:
    def __init__(self, mailManager: MailManager):
        self._mailManager = mailManager

    def init(self):
        pass

    def sendNotificationMail(self, notification: Notification):
        if notification.email:
            self._mailManager.send(notification.getEmail())

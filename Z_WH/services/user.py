import datetime
from typing import List
import string
import bcrypt
from Z_WH.tools.meta import MetaData
from Z_WH.services.notification import NotificationManager, Notification
from Z_WH.tools.randomString import getRandomString

from Z_WH.tools.log import Logger

logger = Logger('user')


class UserManagerError(Exception):
    def __init__(self, message: str):
        self.message = message


class LogKey:
    def __init__(self, **kwargs):
        self.id: str or None = kwargs.get('id')
        self.key: str or None = kwargs.get('key')
        self.userAgent: str or None = kwargs.get('userAgent')
        self.ip: str or None = kwargs.get('ip')

        def getDate(date: str) -> datetime.datetime:
            if date:
                return datetime.datetime.fromisoformat(date)

        self.createdAt: datetime.datetime = getDate(kwargs.get('createdAt'))
        self.lastGenerated: datetime.datetime = getDate(kwargs.get('createdAt'))

    def _hashKey(self):
        self.key = getRandomString(string.ascii_uppercase + string.ascii_lowercase + string.digits + '-', 250)

    def initKey(self, userAgent=None, ip=None):
        now = datetime.datetime.now()
        self.createdAt = now
        self.lastGenerated = now
        self.userAgent = userAgent
        self.ip = ip
        self.id = getRandomString(string.ascii_uppercase + string.digits, 8)
        self._hashKey()

    def regenerate(self):
        self.lastGenerated = datetime.datetime.now()
        self._hashKey()

    def getInfo(self):
        return {
            'id': self.id,
            'key': self.key,
            'userAgent': self.userAgent,
            'ip': self.ip,
            'createdAt': self.createdAt.isoformat(),
            'lastGenerated': self.lastGenerated.isoformat()
        }


class UserManager:
    def __init__(self, notificationManager: NotificationManager):
        self._notificationManager = notificationManager

        self._email: str or None = None
        self._password: bytes or None = None

        self._logKeys: List[LogKey] = []

        self._metaUser = MetaData('user')
        self._metaLogKey = MetaData('login-key')

    def init(self):
        self._loadMetaUser()
        self._loadMetaLogKey()

    def _loadMetaUser(self):
        metaUser = self._metaUser.data
        if metaUser:
            self._email = metaUser.get('email')
            self._password = bytes(metaUser.get('password'), encoding='utf-8')

    def _loadMetaLogKey(self):
        metaLogKeys = self._metaLogKey.data
        if metaLogKeys:
            self._logKeys = [LogKey(**metaLogKey) for metaLogKey in metaLogKeys]

    def _saveMetaUser(self):
        self._metaUser.data = {
            'email': self._email,
            'password': self._password.decode('utf-8')
        }

    def _saveMetaLogKey(self):
        self._metaLogKey.data = [logKey.getInfo() for logKey in self._logKeys]

    def _findKeyById(self, keyId) -> LogKey:
        for logKey in self._logKeys:
            if logKey.id == keyId:
                return logKey
        raise UserManagerError('KEY_NOT_FOUND')

    def _hashPassword(self, password: str):
        passwd = bytes(password, encoding='utf-8')
        self._password = bcrypt.hashpw(passwd, bcrypt.gensalt(12))

    def initUser(self, email: str, password: str):
        self._email = email
        self._hashPassword(password)
        self._saveMetaUser()
        notification = Notification()
        notification.subject = 'Compte initialisé'
        notification.content = 'Le compte sur l\'appareil Z-WaterHeater a bien été reinitialisé !'
        notification.email = self._email
        logger.info(f"User init with email {self._email}")
        self._notificationManager.sendNotificationMail(notification)

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password: str):
        self._hashPassword(password)
        self._saveMetaUser()
        notification = Notification()
        notification.email = self._email
        notification.subject = 'Mot de passe changé'
        notification.content = """Le mot de passe de l'appareil Z-WaterHeater a été changé. S'il ne s'agit pas de 
        vous, veuillez tout de suite réinitialiser l'appareil ! """
        logger.info("User change his password")
        self._notificationManager.sendNotificationMail(notification)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, newEmail):
        notification = Notification()
        notification.email = self._email
        self._email = newEmail
        self._saveMetaUser()
        notification.subject = 'Email changé'
        notification.content = f"""L'email l'appareil Z-WaterHeater a été changé par {newEmail}. S'il ne s'agit pas de 
        vous, veuillez tout de suite réinitialiser l'appareil ! """
        logger.info("User change his email")
        self._notificationManager.sendNotificationMail(notification)

    def login(self, email: str, password: str, userAgent: str or None = None, ip: str or None = None) -> LogKey:
        if self._email != email or not bcrypt.checkpw(bytes(password, encoding='utf-8'), self._password):
            raise UserManagerError('INVALID_CREDENTIAL')
        logKey = LogKey()
        logKey.initKey(userAgent, ip)
        self._logKeys.append(logKey)
        self._saveMetaLogKey()

        notification = Notification()
        date = datetime.datetime.now()
        notification.subject = 'Nouvelle connexion'
        notification.email = self._email
        if userAgent:
            content = f"Nouvelle connexion sur l'appareil {userAgent} ."
        else:
            content = "Nouvelle connexion sur un appareil de nom inconnu ! "
        content += f"\n Depuis {ip} ."
        content += f"\nConnexion le {date.strftime('%d-%m-%y')} à {date.strftime('%H:%M:%S')}."
        notification.content = content
        logger.info("User new login")
        self._notificationManager.sendNotificationMail(notification)

        return logKey

    def checkKey(self, keyId: str, key: str):
        if keyId is None or key is None:
            raise UserManagerError('LOG_KEY_NONE')
        logKey = self._findKeyById(keyId)
        if logKey.key != key:
            raise UserManagerError('INVALID_KEY')

    def regenerateKey(self, keyId: str) -> LogKey:
        logKey = self._findKeyById(keyId)
        logKey.regenerate()
        self._saveMetaLogKey()
        logger.info(f'Renew keyid {keyId}')
        return logKey

    def deleteKey(self, keyId: str):
        for i in range(len(self._logKeys)):
            if self._logKeys[i].id == keyId:
                logger.info(f'Delete keyid {keyId}')
                self._logKeys.pop(i)
                self._saveMetaLogKey()
                return
        raise UserManagerError('KEY_NOT_FOUND')

    def deleteAllKey(self):
        logger.info('Delete all key')
        self._logKeys = []
        self._saveMetaLogKey()

    def getLogKeysInfo(self):
        return [{
            'id': logKey.id,
            'userAgent': logKey.userAgent,
            'ip': logKey.ip,
            'createdAt': logKey.createdAt,
            'lastGenerated': logKey.lastGenerated
        } for logKey in self._logKeys]

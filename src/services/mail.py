import smtplib, ssl

from src.tools.meta import MetaData


class MailManager:
    def __init__(self, config_file='smtp-mail'):
        self._host = None
        self._port = None
        self._login = None
        self._password = None

        self._meta = MetaData(config_file)

        self._context = ssl.create_default_context()

        self.load()

    # Load the SMTP configuration
    def load(self):
        config = self._meta.data
        if config is not None:
            self._host = config.get('host')
            self._port = config.get('port')
            self._login = config.get('login')
            self._password = config.get('password')

    # Save new SMTP configuration
    def saveConfig(self, **kwargs):
        if kwargs.get('host'):
            self._host = kwargs['host']
        if kwargs.get('port'):
            self._port = kwargs['port']
        if kwargs.get('login'):
            self._login = kwargs['login']
        if kwargs.get('password'):
            self._password = kwargs['password']

        self.saveMeta()

    # Get the SMTP configuration
    def getConfig(self):
        if self._meta.data is None:
            return None
        return {
            'host': self._host,
            'port': self._port,
            'login': self._login
        }

    # Save the SMTP configuration in the meta
    def saveMeta(self):
        self._meta.data = {
            'host': self._host,
            'port': self._port,
            'login': self._login,
            'password': self._password
        }

    # Send a mail
    def send(self, mail_from, destination, content):
        with smtplib.SMTP(self._host, self._port) as server:
            server.ehlo()
            server.starttls(context=self._context)
            server.ehlo()
            server.login(self._login, self._password)
            print(server.sendmail(mail_from, destination, content))


mail = MailManager()

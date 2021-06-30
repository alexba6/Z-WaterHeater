from os import getenv
from dotenv import load_dotenv

from .api import app
from .config import DEBUG
from .services import initAllServices, notificationManager
from .services.notification import Notification
from .tools.schedule import run_continuously


load_dotenv()


def setup():
    run_continuously()

    initAllServices()

    app.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)

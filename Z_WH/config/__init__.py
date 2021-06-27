from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEV, PROD, TEST = 'development', 'production', 'test'

DEBUG = getenv('DEBUG') == 'True'

APP_ENV = getenv('APP_ENV')

if APP_ENV not in [DEV, PROD, TEST]:
    APP_ENV = PROD

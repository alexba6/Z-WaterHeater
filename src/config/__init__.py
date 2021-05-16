from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEBUG = getenv('DEBUG') == 'True'

APP_ENV = 'production'

if getenv('APP_ENV') == 'development':
    APP_ENV = 'development'
elif getenv('APP_ENV') == 'test':
    APP_ENV = 'test'

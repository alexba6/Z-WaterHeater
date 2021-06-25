from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEV, PROD, TEST = 'development', 'production', 'test'

DEBUG = getenv('DEBUG') == 'True'

JWT_ALGORITHM = 'HS256'
JWT_KEY = getenv('JWT_KEY')

APP_ENV = getenv('APP_ENV')

if APP_ENV not in [DEV, PROD, TEST]:
    APP_ENV = PROD

print(f'> App running in {APP_ENV}')

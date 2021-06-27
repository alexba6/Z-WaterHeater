from os import getenv
from dotenv import load_dotenv

load_dotenv()

JWT_ALGORITHM = 'HS256'
JWT_KEY = getenv('JWT_KEY')

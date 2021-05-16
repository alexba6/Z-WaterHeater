from os import getenv
from dotenv import load_dotenv

import src.models as models
from src.api import api
from src.config import DEBUG

load_dotenv()


if __name__ == '__main__':
    models.create_all_table()
    api.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)

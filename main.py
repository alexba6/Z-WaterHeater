from os import getenv
from dotenv import load_dotenv

import src.models as models
from src.api import api
from src.config import DEBUG
from src.utils import display
from src.log import info_logger


load_dotenv()


if __name__ == '__main__':
    info_logger.add('APP started !')
    models.create_all_table()
    display.start()

    api.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)



# Z-CE http API
from os import getenv
from dotenv import load_dotenv

import src.models as models
from src.http import api
from src.config import DEBUG
from src.services import display, output
from src.tools.log import info_logger


load_dotenv()


if __name__ == '__main__':
    info_logger.add('APP started !')
    models.create_all_table()

    display.display.start()
    output.start()

    api.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)



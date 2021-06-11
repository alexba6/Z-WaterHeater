# Z-CE http API
from os import getenv
from dotenv import load_dotenv

import src.models as models
from src.api import apiHttp
from src.config import DEBUG
from src.services import operation_state
from src.utils import display, output
from src.tools.log import logger


load_dotenv()

if __name__ == '__main__':
    logger.info('app started')
    models.create_all_table()

    display.display.start()

    output.group_manager.load()
    output.group_manager.init()

    operation_state.operation_sate.load()
    operation_state.operation_sate.switchOn(3)

    apiHttp.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)

# Z-CE http API
from os import getenv
from dotenv import load_dotenv

import src.models as models
from src.api import app
from src.config import DEBUG
from src.services import operation_state, temp_chart, display, outManager
from src.utils import output, temp
from src.tools.log import logger


load_dotenv()

if __name__ == '__main__':
    logger.info('app started')
    models.create_all_table()

    display.display.init()

    output.groupManager.init()
    outManager.outManager.init()

    operation_state.operation_sate.init()

    temp.temp_manager.init()

    temp_chart.temp_chart.init()

    app.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)

from os import getenv
from dotenv import load_dotenv

from .models import create_all_table
from .api import app
from .config import DEBUG
from .services import tempChart, display, outManager
from .utils import output, temp
from .tools.log import logger
from .tools.schedule import run_continuously


load_dotenv()


def setup():
    run_continuously()
    logger.info('app started')

    create_all_table()

    display.display.init()

    temp.temp_manager.init()
    tempChart.temp_chart.init()

    output.groupManager.init()
    outManager.outManager.init()

    app.run(port=getenv('API_PORT'), host=getenv('API_HOST'), debug=DEBUG)

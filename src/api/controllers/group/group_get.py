import sqlalchemy
from ....tools.log import logger
from ...responces import server_error
from ...middlewares import auth, response
from ....models.User import ADMIN
from ....config.database import Session
from ....models.OutputGroup import OutputGroup


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def group_get_all_ctrl(**kwargs):
    try:
        with Session() as session:
            groups = session.query(OutputGroup).all()
            return {
                'groups': [
                    {
                        'id': group.id,
                        'name': group.name,
                        'outputs_id': group.output
                    }
                    for group in groups
                ]
            }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()

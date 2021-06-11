from ....tools.log import logger
from ...responces import server_error
from ...middlewares import format_body, auth, response
from ....models.User import ADMIN
from ....models.OutputGroup import OutputGroup
from src.utils.output import group_manager
from ....config.database import Session


@response.format_json
@format_body.body_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.check_body(['name', 'outputs_id'])
def group_add_ctrl(**kwargs):
    try:
        body = kwargs['body']
        with Session() as session:
            group = OutputGroup()
            group.name = body['name']
            group.output = body['outputs_id']

            session.add(group)
            session.commit()
            group_manager.load()

            return {
                'message': 'Groups added successfully !'
            }, 201
    except Exception as error:
        print(error)
        logger.error(error)
        return server_error.internal_server_error()

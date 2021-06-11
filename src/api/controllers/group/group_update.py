import sqlalchemy
from ....tools.log import logger
from ...responces import server_error
from ...middlewares import auth, format_body, response
from ....models.User import ADMIN
from src.utils.output import group_manager
from ....config.database import Session
from ....models.OutputGroup import OutputGroup


@response.format_json
@format_body.body_json
@format_body.check_body(None, ['name', 'outputs_id'])
@auth.check_user_key
@auth.check_role(ADMIN)
def group_update_ctrl(**kwargs):
    try:
        body = kwargs['body']

        with Session() as session:
            group: OutputGroup = session.execute(
                sqlalchemy.select(OutputGroup).where(OutputGroup.id == kwargs['group_id'])
            ).scalar_one()
            print(body.get('outputs_name'))
            if group:
                if body.get('name'):
                    group.name = body['name']
                if body.get('outputs_id'):
                    print(body['outputs_id'])
                    group.output = body['outputs_id']
                session.add(group)
                session.commit()
                group_manager.load()
                return {
                    'message': 'Group updated !'
                }, 200
            else:
                return {
                    'error': 'GROUP_NOT_FOUND'
                }, 404
    except Exception as error:
        if error.args[0] == 'INVALID_OUTPUTS':
            return {
                "error": "Invalid outputs id",
                "available_outputs_id": ['out 1', 'out 2']
            }, 400
        logger.error(error)
        return server_error.internal_server_error()

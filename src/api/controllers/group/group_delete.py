import sqlalchemy
from ....tools.log import logger
from ...responces import server_error
from ...middlewares import auth, response
from ....models.User import ADMIN
from ....models.OutputGroup import OutputGroup
from ....services.output import group_manager
from ....config.database import Session


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def group_delete_ctrl(**kwargs):
    try:
        group_id = kwargs['group_id']
        with Session() as session:
            group = session.query(OutputGroup).filter(OutputGroup.id == group_id).first()
            if group:
                session.delete(group)
                session.commit()
                group_manager.load()
                return {
                   'message': f"Group {group_id} deleted !"
                }, 200
            else:
                return {
                    'error': "Group not found !"
                }, 404

    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


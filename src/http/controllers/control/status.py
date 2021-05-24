from flask import jsonify

from src.models.User import WRITER
from src.http.middlewares import auth
from src.config import DEBUG
from src.http.responces import server_error
from src.services import output


@auth.check_user_key
@auth.check_role(WRITER)
def status_ctrl(**kwargs):
    try:
        if output.group_manager.exist_groups(kwargs['group_name']):
            state = kwargs['state'].upper()
            if state == 'ON' or state == 'OFF':
                output.group_manager.switch_group(kwargs['group_name'], (True if state == 'ON' else False))
                return jsonify({
                    'message': 'Input ok !'
                }), 200
            else:
                return jsonify({
                    'error': 'State must be a ON or OFF !'
                }), 400
        else:
            return jsonify({
                'error': 'Group does not exist !'
            }), 404
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()

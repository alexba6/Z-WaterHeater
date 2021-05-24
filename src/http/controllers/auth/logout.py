from flask import jsonify
from src.config import DEBUG
from src.config.database import Session
from src.models import AuthorizationKey
from src.http.responces import server_error
from src.http.middlewares import format_body


@format_body.body_json
@format_body.check_body(['key_id', 'key'])
def logout_ctrl(**data):
    try:
        body = data.get('body')
        session = Session()
        authorization_key = session.query(AuthorizationKey) \
            .filter(AuthorizationKey.id == body['key_id']) \
            .first()
        if isinstance(authorization_key, AuthorizationKey):
            if authorization_key.key == body['key']:
                session.delete(authorization_key)
                session.commit()
                return jsonify({
                    'message': 'Logout successfully !'
                }), 200
            else:
                return jsonify({
                    'error': 'KEY_INVALID'
                }), 400
        else:
            return jsonify({
                'error': 'KEY_NOT_FOUND'
            }), 404
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()



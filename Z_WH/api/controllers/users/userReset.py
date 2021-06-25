from ...middlewares import schema, authentification, response

from Z_WH.config.database import Session
from Z_WH.models.User import User, ADMIN


@response.json
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'password': {
            'type': 'string'
        }
    },
    'required': ['password']
})
@authentification.checkUserKey(ADMIN)
def resetUserPasswordCtrl(**kwargs):
    json = kwargs.get('json')
    userId = kwargs.get('userId')
    if userId == kwargs.get('user').id:
        return {
            'error': 'Cannot delete own user !'
        }, 400
    with Session() as session:
        user = session.query(User) \
            .filter(User.id == userId) \
            .first()
        if user is None:
            return {
                'error': 'User not found !'
            }, 400
        user.hash_password(json['password'])
        session.add(user)
        session.commit()
    return {
        'message': 'Password updated successfully !'
    }, 200

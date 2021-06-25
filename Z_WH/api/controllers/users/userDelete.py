from ...middlewares import authentification, response

from Z_WH.config.database import Session
from Z_WH.models.User import User, ADMIN
from Z_WH.models.AuthorizationKey import AuthorizationKey


@response.json
@authentification.checkUserKey(ADMIN)
def delUserCtrl(**kwargs):
    userId = int(kwargs.get('id'))
    if userId == kwargs.get('userId'):
        return {
            'error': 'Cannot delete own user !'
        }, 400
    with Session() as session:
        authKeys = session.query(AuthorizationKey)\
            .fliter(AuthorizationKey.user_id == userId)\
            .all()
        if authKeys:
            for authKey in authKeys:
                session.delete(authKey)
        user = session.query(User) \
            .filter(User.id == userId) \
            .first()
        if user is None:
            return {
                'error': 'User not found !'
            }, 400
        session.delete(user)
        session.commit()

    return {}, 406

from ...middlewares import authentification, response

from ....config.database import Session
from ....models.User import User, ADMIN


@response.json
@authentification.checkUserKey(ADMIN)
def delUserCtrl(**kwargs):
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
        session.delete(user)
        session.commit()

        return {}, 406

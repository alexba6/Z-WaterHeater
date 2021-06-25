from Z_WH.config.database import Session
from Z_WH.api.middlewares import response, authentification
from Z_WH.models.AuthorizationKey import AuthorizationKey


@response.json
@authentification.checkUserKey()
def logoutCtrl(**kwargs):
    with Session() as session:
        key: AuthorizationKey = session.query(AuthorizationKey)\
            .filter(AuthorizationKey.id == kwargs['keyId'])\
            .first()
        session.delete(key)
        session.commit()
        return {
            'message': 'Logout successfully !'
        }, 200

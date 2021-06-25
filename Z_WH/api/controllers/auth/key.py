import datetime

from Z_WH.models import AuthorizationKey
from Z_WH.config.database import Session
from Z_WH.api.middlewares import response, authentification


@response.json
@authentification.checkUserKey()
def regenerateKeyCtrl(**kwargs):
    with Session() as session:
        authorizationKey: AuthorizationKey = session.query(AuthorizationKey) \
                .filter(AuthorizationKey.id == kwargs['keyId']) \
                .first()
        date = datetime.datetime.now()

        authorizationKey.last_generated = date
        key = authorizationKey.generate_key()
        session.add(authorizationKey)
        session.commit()

        return {
            'keyId': authorizationKey.id,
            'newKey': key
        }, 200


@response.json
@authentification.checkUserKey()
def checkKeyCtrl(**kwargs):
    return {
        'message': 'VALID'
    }, 200

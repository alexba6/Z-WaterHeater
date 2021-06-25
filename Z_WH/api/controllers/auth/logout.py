from Z_WH.config.database import Session
from Z_WH.api.middlewares import response, authentification


@response.json
@authentification.checkUserKey()
def logoutCtrl(**kwargs):
    with Session() as session:
        session.delete(session.merge(kwargs['key']))
        session.commit()
        return {
            'message': 'Logout successfully !'
        }, 200

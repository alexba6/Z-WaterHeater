from Z_WH.api.middlewares import schema, authentification, response

from Z_WH.config.database import Session
from Z_WH.models.User import User, ADMIN


def userResponse(user: User):
    return {
        'message': 'User added !',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'createdAt': user.created_at
        }
    }, 201


@response.json
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string'
        },
        'username': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
        'role': {
            'enum': ['W', 'R']
        }
    },
    'required': ['email', 'username', 'password', 'role']
})
@authentification.checkUserKey(ADMIN)
def addUserCtrl(**kwargs):
    json = kwargs.get('json')
    with Session() as session:
        findEmail = session.query(User) \
            .filter(User.email == json['email']) \
            .first()

        if findEmail:
            return {
                       'error': 'Email already taken !'
                   }, 400

        findUsername = session.query(User) \
            .filter(User.username == json['username']) \
            .first()

        if findUsername:
            return {
                       'error': 'Username already taken !'
                   }, 400

        user = User()
        user.email = json['email']
        user.username = json['username']
        user.hash_password(json['password'])
        user.setRole(json['role'])

        session.add(user)
        session.commit()

        return userResponse(user)


@response.json
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string'
        },
        'username': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    },
    'required': ['email', 'username', 'password']
})
@authentification.checkUserToken
def addAdminCtrl(**kwargs):
    json = kwargs.get('json')

    with Session() as session:
        admins = session.query(User) \
            .filter(User.role == 'A') \
            .all()
        if len(admins) > 0:
            for admin in admins:
                session.delete(admin)
            session.commit()

        admin = User()
        admin.email = json['email']
        admin.username = json['username']
        admin.hash_password(json['password'])
        admin.role = ADMIN
        session.add(admin)
        session.commit()
        return userResponse(admin)

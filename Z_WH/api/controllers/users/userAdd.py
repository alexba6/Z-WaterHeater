from Z_WH.api.middlewares import schema, authentification, response

from Z_WH.services import userManager


@response.json
@authentification.checkUserToken
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    },
    'required': ['email', 'password']
})
def initUser(**kwargs):
    json = kwargs.get('json')
    userManager.initUser(json['email'], json['password'])
    return {
        'message': 'User added !'
    }, 201

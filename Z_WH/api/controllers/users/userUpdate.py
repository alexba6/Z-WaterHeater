from Z_WH.api.middlewares import schema, authentification, response

from Z_WH.services import userManager


@response.json
@authentification.checkUserKey
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    }
})
def updateUser(**kwargs):
    json = kwargs.get('json')
    email = json.get('email')
    if email:
        userManager.email = email
    password = json.get('password')
    if password:
        userManager.password = password
    return {
        'message': 'User updated !'
    }, 200

from flask import request

from Z_WH.api.middlewares import response, schema
from Z_WH.services import userManager


@response.json
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
def loginCtrl(**kwargs):
    json = kwargs.get('json')
    logKey = userManager.login(json['email'], json['password'], request.user_agent.string, request.remote_addr)
    return {
        'message': 'Connected !',
        'keyId': logKey.id,
        'key': logKey.key
    }, 200

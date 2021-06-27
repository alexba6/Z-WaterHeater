from Z_WH.services import verificationCodeManager
from Z_WH.api.middlewares import response, schema, authentification


@response.json
def generateCodeCtrl():
    valid_time = 6
    verificationCodeManager.generateCode(60)
    return {
        'message': 'Code generated !',
        'validTime': valid_time
    }, 200


@response.json
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'code': {
            'type': 'string'
        }
    },
    'required': ['code']
})
def checkCodeCtrl(**kwargs):
    json = kwargs.get('json')
    verificationCodeManager.verifyCode(json['code'])
    expirationTime = 60*20
    token = authentification.createToken(expirationTime)
    return {
        'message': 'Verification ok',
        'token': token,
        'validTime': expirationTime
    }, 200

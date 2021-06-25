from flask import request
import json
from jsonschema import validate


def schemaValidator(schema):
    def wrapper(func):
        def inner(*arg, **kwargs):
            body = json.loads(request.get_data())
            validate(body, schema)
            kwargs['json'] = body
            return func(*arg, **kwargs)
        return inner
    return wrapper

import json
from flask import request

BODY_AND, BODY_OR = 'and', 'or'


def body_json(function):
    def wrapper():
        try:
            return function(body=json.loads(request.get_data()))
        except:
            return {
                'error': 'JSON body required !'
            }, 400
    return wrapper


def check_body(allow_items, operator=BODY_AND):
    def decorator(function):
        def wrapper(**kwargs):
            body = kwargs.get('body')
            data = {}
            for allow_item in allow_items:
                body_item = body.get(allow_item)
                if body_item:
                    data[allow_item] = body[allow_item]
                elif operator == BODY_AND:
                    return {
                        'error': 'Body schema violation !',
                        'allow_items': allow_items,
                        'operator': operator
                    }, 400
            kwargs['body'] = data
            return function(**kwargs)
        return wrapper
    return decorator


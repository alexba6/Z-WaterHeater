import json
from flask import request, jsonify


def body_json(function):
    def wrapper(**kwargs):
        try:
            kwargs['body'] = json.loads(request.get_data())
            return function(**kwargs)
        except Exception as error:
            print(error)
            return jsonify({
                'error': 'JSON body required !'
            }), 400
    return wrapper


def check_body(allow_items_and=None, allow_items_or=None, or_min_length=1):
    def decorator(function):
        def wrapper(**kwargs):
            body = kwargs.get('body')
            data = {}
            error = False
            or_length = 0
            if allow_items_and:
                for allow_item_and in allow_items_and:
                    body_item = body.get(allow_item_and)
                    if body_item:
                        data[allow_item_and] = body[allow_item_and]
                    else:
                        error = False
            if allow_items_or:
                for allow_item_or in allow_items_or:
                    body_item = body.get(allow_item_or)
                    if body_item:
                        data[allow_item_or] = body[allow_item_or]
                        or_length += 1

            if error or (allow_items_or and or_length < or_min_length):
                return jsonify({
                    'error': 'Body schema violation !',
                    'allow_items_and': allow_items_and,
                    'allow_items_and': allow_items_or
                }), 400

            kwargs['body'] = data
            return function(**kwargs)
        return wrapper
    return decorator

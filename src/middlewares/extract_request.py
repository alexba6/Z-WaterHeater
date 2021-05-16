import json

BODY_AND, BODY_OR = 'and', 'or'


def body_json(request):
    def decorator(function):
        def wrapper():
            return function(json.loads(request.get_data()))
        return wrapper
    return decorator


def check_body(allow_items, operator=BODY_AND):
    def decorator(function):
        def wrapper(body):
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
            print(data)
            return function(data)
        return wrapper
    return decorator


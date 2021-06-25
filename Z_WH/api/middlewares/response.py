from flask import jsonify, make_response


def json(func):
    def wrapper(*arg, **kwargs):
        jsonResponse, status = func(*arg, **kwargs)
        response = make_response(jsonify(jsonResponse), status)
        response.headers['Server'] = 'Z-WH API'
        return response
    return wrapper

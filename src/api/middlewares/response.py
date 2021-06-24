from flask import jsonify, make_response


def format_json(function):
    def wrapper(*arg, **kwargs):
        json, status = function(*arg, **kwargs)
        response = make_response(jsonify(json), status)
        response.headers['Server'] = 'Z-CE API'
        return response
    return wrapper


def json(func):
    def wrapper(*arg, **kwargs):
        jsonResponse, status = func(*arg, **kwargs)
        response = make_response(jsonify(jsonResponse), status)
        response.headers['Server'] = 'Z-CE API'
        return response
    return wrapper

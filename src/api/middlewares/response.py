from flask import jsonify, make_response
from ..responces import server_error
from ...config import DEBUG


def make_json_response(json, status):
    try:
        response = make_response(jsonify(json), status)
        response.headers['Server'] = 'Z-CE API'
        return response
    except Exception as error:
        if DEBUG:
            print(error)
        return server_error.internal_server_error()


def format_json(function):
    def wrapper(**kwargs):
        return make_json_response(*function(**kwargs))
    return wrapper

from flask import jsonify

def internal_server_error():
    return jsonify({
        'error': 'An error occurred on the server !'
    }), 500

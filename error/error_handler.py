from flask import jsonify


def handle_not_found_error(error):
    return jsonify({
        'message': 'Not Found',
        'error': str(error)
        }), 404


def handle_internal_server_error(error):
    return jsonify({
        'message': 'Internal Server Error',
        'error': str(error)
        }), 500

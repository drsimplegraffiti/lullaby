from flask import Blueprint, request, jsonify

health = Blueprint('health', __name__)

@health.route('/', methods=['GET'])
def health_route():
    try:
        return jsonify({
            'message': 'Server is healthy'
        }), 200
    except Exception as e:
        # Handle exception here
        print(f"An error occurred during health check: {str(e)}")
        return jsonify({
            'message': 'An error occurred during health check'
        }), 500
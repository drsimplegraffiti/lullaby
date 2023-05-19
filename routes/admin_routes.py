from flask import Blueprint, request, jsonify
from models.users import User
from models.blogs import Blog
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.admin_controller import admin_dashboard_controller

admin_routes = Blueprint('admin_routes', __name__)

# admin_dashboard_controller(user_id)


@admin_routes.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    try:
        # get user id from token
        user_id = get_jwt_identity()

        response = admin_dashboard_controller(user_id['id'])
        if not response:
            return jsonify({
                'message': 'An error occurred during admin dashboard'
            }), 500

        return response
    except Exception as e:
        print(f"An error occurred during admin dashboard: {str(e)}")
        return None

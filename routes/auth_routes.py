from flask import Blueprint, request, jsonify
from controllers.auth_controller import signup_controller, login_controller, verify_user_controller, resend_verification_code_controller
from models.users import User
from validation.auth_validation import SignupSchema, loginSchema, verifyEmailSchema
from utils.email_sender import send_email
from string import Template
from pathlib import Path
from utils.verification_generator import generate_verification_code
from flask_jwt_extended import jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)

# signup_route

@auth.route('/signup', methods=['POST'])
def signup_route():
    try:
        # Load and validate data using the SignupSchema
        schema = SignupSchema()
        data = request.get_json()
        errors = schema.validate(data)
        if errors:
            # Return error response for invalid data
            return jsonify({
                'message': 'Invalid data',
                'errors': errors
            }), 400

        username = data['username']
        email = data['email']
        password = data['password']

        # Check if user exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return jsonify({
                'message': 'User already exists'
            }), 409
        otp = generate_verification_code()
        print(otp)
        user = signup_controller(username, email, password, otp)
        if user:
            subject='Welcome to Flask Blog'
            html_template = Template(Path('templates/signup.html').read_text())
            html_content = html_template.substitute({'username': username, 'otp': otp})
            send_email(subject, email, html_content)
            return jsonify({
                'message': 'User created successfully',
                'user': user.serialize()
            }), 201
        else:
            return jsonify({
                'message': 'User not created'
            }), 500
    except Exception as e:
        error_message = f"An error occurred during signup: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during signup',
            'error': error_message
        }), 500

# login_route

@auth.route('/login', methods=['POST'])
def login_route():
    try:
        schema = loginSchema()
        data = request.get_json()
        errors = schema.validate(data) #we are validating the data that we are getting from the request
        if errors:
            return jsonify({
                'message': 'Invalid data',
                'errors': errors
            }), 400

        email = data['email']
        password = data['password']

        response = login_controller(email, password)
        if response:
            return response
        else:
            return jsonify({
                'message': 'Login failed'
            }), 401
    except Exception as e:
        error_message = f"An error occurred during login: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during login',
            'error': error_message
        }), 500
    
# verify_route
@auth.route('/verify', methods=['POST'])
@jwt_required()
def verify_route():
    try:
        schema = verifyEmailSchema()
        data = request.get_json()
        errors = schema.validate(data)
        if errors:
            # Return error response for invalid data
            return jsonify({
                'message': 'Invalid data',
                'errors': errors
            }), 400
        user = get_jwt_identity()
        
        otp = data['verification_code']
        response = verify_user_controller(user['email'], otp)
        if response:
            return response
        else:
            return jsonify({
                'message': 'Verification failed'
            }), 401

    except Exception as e:
        error_message = f"An error occurred during verification: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during verification',
            'error': error_message
        }), 500
    

#resend verification code
@auth.route('/resend', methods=['POST'])
@jwt_required()
def resend_route():
    try:
        user = get_jwt_identity()
        print(user)
        user_ = resend_verification_code_controller(user['email'])
        print(user_)

        #send email
        subject='Welcome to Flask Blog'
        html_template = Template(Path('templates/signup.html').read_text())
        html_content = html_template.substitute({'username': user['username'], 'otp': user_.verification_code})
        send_email(subject, user['email'], html_content)
        return jsonify({
            'message': 'Verification code sent successfully'
        }), 200
    

    except Exception as e:
        error_message = f"An error occurred during verification: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during verification',
            'error': error_message
        }), 500
    

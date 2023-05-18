from models.users import User
from config.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from utils.verification_generator import generate_verification_code, generate_reset_token


def signup_controller(username, email, password, otp):
    try:
        # Hash password
        hash_password = generate_password_hash(password)

        # Create user
        user = User(username=username, email=email, password=hash_password, verification_code=otp)
        db.session.add(user)
        db.session.commit()
        print(f"User {user.id} created successfully")
        return user
    except Exception as e:
        print(f"An error occurred during signup: {str(e)}")
        return None

def login_controller(email, password):
    try:
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'message': 'User does not exist'
            }), 404

        # Check if password is correct
        if not check_password_hash(user.password, password):
            return jsonify({
                'message': 'Incorrect password'
            }), 401

        # Create access token
        access_token = create_access_token(identity={
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

        # Set access token in cookies
        response = jsonify({
            'message': 'Login successful',
            'access_token': access_token
        })

        set_access_cookies(response, access_token)

        return response

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")
        return None
    

# verify code
def verify_user_controller(email, verification_code):
    try:

        user = User.query.filter_by(email=email).first()
        if user.is_verified:
            return jsonify({
                'message': 'User already verified'
            }), 409
        
        if user.verification_code != verification_code:
            return jsonify({
                'message': 'Incorrect verification code'
            }), 401

        if not user:
            return jsonify({
                'message': 'User does not exist'
            }), 404

        user.verification_code = None
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        print(f"User {user.id} verified successfully")

        return jsonify({
            'message': 'User verified successfully'
        }), 200
    except Exception as e:
        print(f"An error occurred during verification: {str(e)}")
        return None
 

 # resend verification code
def resend_verification_code_controller(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'message': 'User does not exist'
            }), 404

        otp = generate_verification_code()
        user.verification_code = otp
        user.is_verified = False
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        print(f"An error occurred during resending verification code: {str(e)}")
        return None
    

# forgot password
def forgot_password_controller(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'message': 'User does not exist'
            }), 404

        #generate token link for password reset
        reset_token = generate_reset_token()
        user.reset_token = reset_token
        print({user.reset_token})
        db.session.add(user)
        db.session.commit()
        link = "http://localhost:3000/reset-password/" + reset_token
        return link
    except Exception as e:
        print(f"An error occurred during forgot password: {str(e)}")
        return None

# reset password
def reset_password_controller(reset_token, password):
    try:
        user = User.query.filter_by(reset_token=reset_token).first()
        if not user:
            return jsonify({
                'message': 'User does not exist'
            }), 404

        # Hash password
        hash_password = generate_password_hash(password)
        user.password = hash_password
        user.reset_token = None
        db.session.add(user)
        db.session.commit()
        print(f"User {user.id} password reset successfully")
        return user
    except Exception as e:
        print(f"An error occurred during password reset: {str(e)}")
        return None
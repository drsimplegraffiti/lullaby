import string
import secrets
from random import randint

# generate verification otp code
def generate_verification_code():
    try:
        # Generate random 6 digit number
        otp = randint(100000, 999999)
        print(f"Generated otp: {otp}")
        return otp
    except Exception as e:
        print(f"An error occurred during otp generation: {str(e)}")
        return None



# Generate reset token for password reset

def generate_reset_token():
    try:
        # Generate a random 32-character token using URL-safe characters
        token = ''.join(secrets.choice(string.ascii_letters +
                        string.digits + '-_') for _ in range(158))
        print(f"Generated reset token: {token}")
        return token
    except Exception as e:
        print(f"An error occurred during reset token generation: {str(e)}")
        return None

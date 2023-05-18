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
    
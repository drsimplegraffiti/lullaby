# Define a schema for signup validation
from marshmallow import Schema, fields, ValidationError

class SignupSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

class loginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class verifyEmailSchema(Schema):
    verification_code = fields.String(required=True)
    email = fields.Email(required=True)

# Define a schema for signup validation
from marshmallow import Schema, fields, ValidationError


class BlogSchema(Schema):
    title = fields.String(required=True)
    body = fields.String(required=True)

from config.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, index=True)
    profile_image = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    user_role = db.Column(db.String(64), default='user')
    reset_token = db.Column(db.String(255), nullable=True)
    verification_code = db.Column(db.String(6), nullable=True)


    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_image': self.profile_image,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'user_role': self.user_role,
            'reset_token': self.reset_token,
            
        }

    
from config.extensions import db, jwt
from flask import Flask
import os
from dotenv import load_dotenv
from datetime import timedelta

from error.error_handler import handle_not_found_error, handle_internal_server_error

# import routes
from routes.health import health
from routes.auth_routes import auth
from routes.blog_routes import blog
from routes.admin_routes import admin_routes

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # configure jwt
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(
        days=7)  # JWTs will expire after 7 days

    db_username = os.getenv('DATABASE_USERNAME')
    db_password = os.getenv('DATABASE_PASSWORD')
    db_host = os.getenv('DATABASE_HOST')
    db_name = os.getenv('DATABASE_NAME')
    db_port = os.getenv('DATABASE_PORT')

    #mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

    #mount routes
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(blog, url_prefix='/api/blog')
    app.register_blueprint(admin_routes, url_prefix='/api/admin')
    app.register_blueprint(health)

    #register error handlers
    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(500, handle_internal_server_error)


    db.init_app(app)
    jwt.init_app(app)
    #print db connection if successful
    with app.app_context(): #the app context is needed to access the db
        print(db.engine.url)
        # check if db connection is successful
        try:
            db.engine.connect()
            print('DB connection successful')
        except Exception as e:
            print(f'Error while connecting to the database: {e}')
    return app

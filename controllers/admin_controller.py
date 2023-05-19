from models.users import User
from models.blogs import Blog
from config.extensions import db
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import jsonify


# admin dashboard for all users, blogs. Only for admin
def admin_dashboard_controller(user_id):
    try:
        # check if user is admin
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'message': 'User does not exist'
            }), 404
        if user.user_role != 'admin':
            return jsonify({
                'message': 'User is not admin, you cannot access this route'
            }), 401

        # get all users
        users = User.query.all()
        users_list = []
        for user in users:
            user_dict = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            users_list.append(user_dict)

        # get all blogs
        blogs = Blog.query.all()
        blogs_list = []
        for blog in blogs:
            blog_dict = {
                'id': blog.id,
                'title': blog.title,
                'body': blog.body,
                'user_id': blog.user_id
            }
            blogs_list.append(blog_dict)

        return jsonify({
            'blogs': blogs_list,
            'users': users_list,
            'users_count': len(users_list),
            'blogs_count': len(blogs_list),
        }), 200

    except Exception as e:
        print(f"An error occurred during admin dashboard: {str(e)}")
        return None
    finally:
        db.session.close()

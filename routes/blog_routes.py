from flask import Blueprint, request, jsonify
from controllers.blogs_controller import create_blog_controller, get_all_blogs_controller, get_blog_controller, update_blog_controller, delete_blog_controller
from models.blogs import Blog
from validation.blog_validation import BlogSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

blog = Blueprint('blog', __name__)

# create_blog_route


@blog.route('/create', methods=['POST'])
@jwt_required()
def create_blog_route():
    try:
        # Load and validate data using the BlogSchema
        schema = BlogSchema()
        data = request.get_json()
        errors = schema.validate(data)
        if errors:
            # Return error response for invalid data
            return jsonify({
                'message': 'Invalid data',
                'errors': errors
            }), 400

        title = data['title']
        body = data['body']
        user_id = get_jwt_identity()

        # Create blog
        blog = create_blog_controller(title, body, user_id['id'])
        if blog:
            return jsonify({
                'message': 'Blog created successfully',
                'blog': blog.serialize()
            }), 201
        else:
            return jsonify({
                'message': 'Blog not created'
            }), 500
    except Exception as e:
        error_message = f"An error occurred during blog creation: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during blog creation',
            'error': error_message
        }), 500


# get_all_blogs_route
@blog.route('/all', methods=['GET'])
def get_all_blogs_route():
    try:
        # Get all blogs
        blogs = get_all_blogs_controller()
        if blogs:
            return jsonify({
                'count': len(blogs),
                'message': 'Blogs retrieved successfully😊',
                'blogs': [blog.serialize() for blog in blogs],
            }), 200
        else:
            return jsonify({
                'message': 'Blogs not retrieved'
            }), 500
    except Exception as e:
        error_message = f"An error occurred while getting all blogs: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred while getting all blogs',
            'error': error_message
        }), 500


@blog.route('/<int:blog_id>', methods=['GET'])
def get_blog_route(blog_id):
    try:
        # Get blog
        blog = get_blog_controller(blog_id)
        if blog:
            return jsonify({
                'message': 'Blog retrieved successfully😊',
                'blog': blog.serialize()
            }), 200
        else:
            return jsonify({
                'message': 'Blog not retrieved'
            }), 500
    except Exception as e:
        error_message = f"An error occurred while getting blog: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred while getting blog',
            'error': error_message
        }), 500


@blog.route('/<int:blog_id>', methods=['PUT'])
@jwt_required()
def update_blog_route(blog_id):
    try:
        # Get blog
        blog = get_blog_controller(blog_id)
        if blog:
            # Load and validate data using the BlogSchema
            schema = BlogSchema()
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                # Return error response for invalid data
                return jsonify({
                    'message': 'Invalid data',
                    'errors': errors
                }), 400

            title = data['title']
            body = data['body']
            user_id = get_jwt_identity()

            # Update blog
            blog = update_blog_controller(blog_id, title, body, user_id['id'])
            if blog:
                return jsonify({
                    'message': 'Blog updated successfully',
                    'blog': blog.serialize()
                }), 201
            else:
                return jsonify({
                    'message': 'Blog not updated'
                }), 500
        else:
            return jsonify({
                'message': 'Blog not retrieved'
            }), 500
    except Exception as e:
        error_message = f"An error occurred during blog update: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during blog update',
            'error': error_message
        }), 500


@blog.route('/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def delete_blog_route(blog_id):
    try:
        # Get blog
        blog = get_blog_controller(blog_id)
        if blog:
            user_id = get_jwt_identity()
            # Delete blog
            blog = delete_blog_controller(blog_id, user_id['id'])
            if blog:
                return jsonify({
                    'message': 'Blog deleted successfully',
                    'blog': blog.serialize()
                }), 201
            else:
                return jsonify({
                    'message': 'Blog not deleted'
                }), 500
        else:
            return jsonify({
                'message': 'Blog not retrieved'
            }), 500
    except Exception as e:
        error_message = f"An error occurred during blog deletion: {str(e)}"
        print(error_message)
        return jsonify({
            'message': 'An error occurred during blog deletion',
            'error': error_message
        }), 500

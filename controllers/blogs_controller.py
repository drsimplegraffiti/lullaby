from models.blogs import Blog
from config.extensions import db
from flask import jsonify


def create_blog_controller(title, body, user_id):
    try:
        # Create blog
        blog = Blog(title=title, body=body, user_id=user_id)
        db.session.add(blog)
        db.session.commit()
        print(f"Blog {blog.id} created successfully")
        return blog
    except Exception as e:
        print(f"An error occurred during blog creation: {str(e)}")
        return None


def get_all_blogs_controller():
    try:
        # Get all blogs
        blogs = Blog.query.all()
        return blogs
    except Exception as e:
        print(f"An error occurred while getting all blogs: {str(e)}")
        return None


def get_blog_controller(blog_id):
    try:
        # Get blog
        blog = Blog.query.filter_by(id=blog_id).first()
        return blog
    except Exception as e:
        print(f"An error occurred while getting blog: {str(e)}")
        return None


def update_blog_controller(blog_id, title, body, user_id):
    try:
       # check if blog exists
        blog = Blog.query.filter_by(id=blog_id).first()
        if not blog:
            return None
        # check if user is the owner of the blog
        if blog.user_id != user_id:
            return None
        # update blog
        blog.title = title
        blog.body = body
        db.session.commit()
        return blog
    except Exception as e:
        print(f"An error occurred while updating blog: {str(e)}")
        return None
    
def delete_blog_controller(blog_id, user_id):
    try:
       # check if blog exists
        blog = Blog.query.filter_by(id=blog_id).first()
        if not blog:
            return None
        # check if user is the owner of the blog
        if blog.user_id != user_id:
            return None
        # delete blog
        db.session.delete(blog)
        db.session.commit()
        return blog
    except Exception as e:
        print(f"An error occurred while deleting blog: {str(e)}")
        return None

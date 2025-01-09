from flask import Blueprint, request, jsonify, abort
from models import Post
from exts import db

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'title': post.title, 'content': post.content, 'pub_date': post.pub_date} for post in posts])

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'title': post.title, 'content': post.content, 'pub_date': post.pub_date})

@posts_bp.route('/', methods=['POST'])
def create_post():
    if not request.json or not 'title' in request.json or not 'content' in request.json:
        abort(400)  # bad request
    post = Post(title=request.json['title'], content=request.json['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'id': post.id}), 201

# @posts_bp.route('/<int:post_id>', methods=['PUT'])
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if not request.json:
#         abort(400)
#     post.title = request.json.get('title', post.title)
#     post.content = request.json.get('content', post.content)
#     db.session.commit()
#     return jsonify({'message': 'Post updated'})

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})
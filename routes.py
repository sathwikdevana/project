from flask import request, jsonify
from app import app, db
from app.models import User, Post, Comment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully."), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

# Create Post
@app.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_post = Post(title=data['title'], content=data['content'], author_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(message="Post created successfully."), 201

# Get All Posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": post.id, "title": post.title, "content": post.content, "author_id": post.author_id} for post in posts]), 200

# Get Single Post
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({"id": post.id, "title": post.title, "content": post.content, "author_id": post.author_id}), 200

# Update Post
@app.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    data = request.get_json()
    post = Post.query.get_or_404(id)
    if post.author_id != get_jwt_identity():
        return jsonify(message="Unauthorized"), 403
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify(message="Post updated successfully."), 200

# Delete Post
@app.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author_id != get_jwt_identity():
        return jsonify(message="Unauthorized"), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify(message="Post deleted successfully."), 200

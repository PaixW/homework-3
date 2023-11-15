from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('homeworkiii.db')  # Replace with your actual database name
cursor = conn.cursor()

# Users Routes

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify({'users': users})

# Get a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'message': 'User not found'}), 404

# Add a new user
@app.route('/users', methods=['POST'])
def add_new_user():
    data = request.get_json()
    username = data['username']
    role = data['role']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO users (username, role, created_at) VALUES (?, ?, ?)", (username, role, created_at))
    conn.commit()

    return jsonify({'message': 'User added successfully'})

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    data = request.get_json()
    username = data['username']
    role = data['role']

    cursor.execute("UPDATE users SET username=?, role=? WHERE id=?", (username, role, user_id))
    conn.commit()

    return jsonify({'message': 'User updated successfully'})

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

    return jsonify({'message': 'User deleted successfully'})


# Posts Routes

# Get all posts
@app.route('/posts', methods=['GET'])
def get_all_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return jsonify({'posts': posts})

# Get a specific post
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    cursor.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = cursor.fetchone()
    if post:
        return jsonify({'post': post})
    else:
        return jsonify({'message': 'Post not found'}), 404

# Add a new post
@app.route('/posts', methods=['POST'])
def add_new_post():
    data = request.get_json()
    title = data['title']
    body = data['body']
    user_id = data['user_id']
    status = data['status']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO posts (title, body, user_id, status, created_at) VALUES (?, ?, ?, ?, ?)",
                   (title, body, user_id, status, created_at))
    conn.commit()

    return jsonify({'message': 'Post added successfully'})

# Update a post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_existing_post(post_id):
    data = request.get_json()
    title = data['title']
    body = data['body']
    status = data['status']

    cursor.execute("UPDATE posts SET title=?, body=?, status=? WHERE id=?", (title, body, status, post_id))
    conn.commit()

    return jsonify({'message': 'Post updated successfully'})

# Delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()

    return jsonify({'message': 'Post deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
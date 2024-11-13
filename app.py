from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///repositories.db'
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Repository model with user association
class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    file_paths = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('repositories', lazy=True))

# Database initialization
@app.before_request
def create_tables():
    db.create_all()

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# User signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 409
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    return jsonify({"message": "Invalid email or password"}), 401

@app.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'GET':
        return jsonify({"email": user.email}) if user else jsonify({"message": "User not found"}), 404

    elif request.method == 'PUT':
        data = request.json
        if data.get('email'):
            user.email = data['email']
        if data.get('password'):
            user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({"message": "Profile updated successfully."}), 200

    elif request.method == 'DELETE':
        try:
            if not user:
                return jsonify({"message": "User not found"}), 404
            
            # Log the user info before deletion (for debugging)
            print(f"Attempting to delete user: {user.email}")
            
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
            return jsonify({"message": "Account deleted successfully"}), 200
        except Exception as e:
            print(f"Error deleting account: {e}")  # Log the error for debugging
            return jsonify({"message": f"Deletion is not Allowed: Please Make Sure All The Added Repositories Must be Deleted Before Deletion of Your Account !"}), 500

# Repository management
@app.route('/repos', methods=['GET', 'POST'])
def manage_repos():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']
    if request.method == 'GET':
        sort_by = request.args.get('sort_by', 'id')
        search_term = request.args.get('search', '').lower()

        query = Repository.query.filter_by(user_id=user_id)
        if search_term:
            query = query.filter((Repository.name.ilike(f'%{search_term}%')) |
                                 (Repository.description.ilike(f'%{search_term}%')))

        repos = query.order_by(Repository.created_at.desc() if sort_by == 'date' else Repository.id).all()
        return jsonify([{
            "id": repo.id, "name": repo.name, "description": repo.description,
            "file_paths": repo.file_paths, "created_at": repo.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for repo in repos])

    elif request.method == 'POST':
        name, description = request.form.get('name'), request.form.get('description')
        file_paths = []

        if 'files[]' not in request.files:
            return jsonify({"message": "No files uploaded"}), 400

        for file in request.files.getlist('files[]'):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            file_paths.append(save_path)

        new_repo = Repository(name=name, description=description,
                              file_paths=",".join(file_paths), user_id=user_id)
        db.session.add(new_repo)
        db.session.commit()
        return jsonify({"message": "Repository added successfully"}), 201

# Repository actions (update, delete)
@app.route('/repos/<int:repo_id>', methods=['PUT', 'DELETE'])
def repo_actions(repo_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    repo = Repository.query.get(repo_id)
    if not repo or repo.user_id != session['user_id']:
        return jsonify({"message": "Repository not found or unauthorized"}), 404

    if request.method == 'DELETE':
        db.session.delete(repo)
        db.session.commit()
        return jsonify({"message": "Repository deleted successfully"}), 200
    
    elif request.method == 'PUT':
        data = request.json
        repo.name, repo.description = data.get('name'), data.get('description')
        db.session.commit()
        return jsonify({"message": "Repository updated successfully"}), 200

# User logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200

# Repo management page
@app.route('/repos-page')
def repos_page():
    if 'user_id' in session:
        return render_template('repos.html')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

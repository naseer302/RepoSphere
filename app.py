from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import secrets

app = Flask(__name__)
session_key = secrets.token_hex(16)
app.secret_key = session_key  # this is a secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///repositories.db'
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Define a Repository model
class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    file_paths = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables
@app.before_request
def create_tables():
    db.create_all()

# Render the landing page
@app.route('/')
def index():
    return render_template('index.html')

# Handle user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        session['user_id'] = user.id
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"message": "Invalid email or password"}), 401

# Handle user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 409
    new_user = User(email=data['email'], password=data['password'])  # Hash password in production
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201
    
# Render the repo management page
@app.route('/repos-page')
def repos_page():
    if 'user_id' in session:
        return render_template('repos.html')
    return redirect(url_for('index'))

# Handle User Profile 
@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'GET':
        # Send current user email in the response
        return jsonify({"email": user.email}), 200

    elif request.method == 'PUT':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Update email if provided
        if email:
            user.email = email
        
        # Update password only if provided
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()
        return jsonify({"message": "Profile updated successfully."}), 200

#repo add, update funtionality with searching and sorting
@app.route('/repos', methods=['GET', 'POST'])
def manage_repos():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']
    
    if request.method == 'GET':
        sort_by = request.args.get('sort_by', 'id')
        search_term = request.args.get('search', '').lower()

        query = Repository.query.filter_by(user_id=user_id)  # Filter by user ID
        if search_term:
            query = query.filter((Repository.name.ilike(f'%{search_term}%')) | 
                                 (Repository.description.ilike(f'%{search_term}%')))

        if sort_by == 'date':
            repos = query.order_by(Repository.created_at.desc()).all()
        else:
            repos = query.order_by(Repository.id).all()

        return jsonify([{
            "id": repo.id, 
            "name": repo.name, 
            "description": repo.description, 
            "file_paths": repo.file_paths,
            "created_at": repo.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for repo in repos])
    
    elif request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        file_paths = []

        if 'files[]' not in request.files:
            return jsonify({"message": "No files uploaded"}), 400

        for file in request.files.getlist('files[]'):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            file_paths.append(save_path)

        new_repo = Repository(
            name=name, 
            description=description,
            file_paths=",".join(file_paths),
            user_id=user_id  # Associate the repository with the logged-in user
        )
        db.session.add(new_repo)
        db.session.commit()

        return jsonify({"message": "Repository added successfully"}), 201

    
# Handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200


if __name__ == '__main__':
    app.run(debug=True)

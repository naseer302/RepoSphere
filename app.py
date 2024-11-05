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


if __name__ == '__main__':
    app.run(debug=True)

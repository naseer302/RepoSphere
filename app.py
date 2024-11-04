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


if __name__ == '__main__':
    app.run(debug=True)

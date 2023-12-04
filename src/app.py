import os
from flask import Flask, request, jsonify, make_response, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
import dotenv 
from auth.guard import token_required
from auth.forms import CredentialsForm
from models import db, User
from flask_wtf.csrf import generate_csrf
from flask_cors import CORS

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('DEBUG')
bcrypt = Bcrypt(app)
db.init_app(app)

# Create tables and seed a test user
with app.app_context():
    db.create_all()
    # Check if the test user already exists
    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        # If the test user doesn't exist, create it
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        new_test_user = User(username='testuser', password=hashed_password)
        db.session.add(new_test_user)
        db.session.commit()

# Route to get CSRF token
@app.route('/csrf', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return jsonify({ 'csrf_token': csrf_token })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    form = CredentialsForm(request.form)
    # return 401 if username or password is not provided or fails validation
    if not form.validate_on_submit():
        print("Form validation failed")
        print(form.errors)
        abort(403, 'Authentication failed.')
    # looking for the user in the database
    user = User.query.filter_by(username=form.username.data).first()
    # return 401 if user not found in the database
    if not user: abort(403, 'Authentication failed.')
    # comparing passwords (hashed)
    if not bcrypt.check_password_hash(user.password, form.password.data): abort(403, 'Authentication failed.')
    # generate token if user found
    payload = {
        'user': request.form['username'],
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return jsonify({ 'token': token })

@app.route('/logout')
def logout():
    return jsonify({ 'message': 'Successfully logged out' })

# Protecting the route with jwt
@app.route('/protected')
@token_required
def protected(current_user):
    return jsonify({ 'message': f'Hello {current_user.username}!' })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'), debug=os.getenv('DEBUG'))
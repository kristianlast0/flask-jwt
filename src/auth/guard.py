from flask import request, jsonify
from functools import wraps
import jwt, os
from models import User

def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        jwt_token = None
        # jwt is passed in the request header
        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Bearer '): return jsonify({ 'error': 'Invalid token format' }), 401
        jwt_token = authorization_header.split()[1]
        # return 401 if token is not passed
        if not jwt_token: return jsonify({ 'error': 'Token is missing' }), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(jwt_token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            # fetch the user to whom the token belongs
            current_user = User.query.filter_by(username=data['user']).first()
            # if user not found
            if not current_user: return jsonify({ 'error': 'User not found' }), 401
            # returns the current logged in users contex to the routes
            return fn(current_user, *args, **kwargs)
        # throws exception if token is expired
        except jwt.ExpiredSignatureError:
            return jsonify({ 'error': 'Token has expired' }), 401
        # throws exception if token does not match
        except jwt.InvalidTokenError:
            return jsonify({ 'error': 'Invalid token' }), 401
        # return 401 if token is not valid
        except Exception as e:
            return jsonify({ 'error': 'Token is invalid' }), 401
    return decorated
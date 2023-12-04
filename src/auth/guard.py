from flask import request, jsonify
from functools import wraps
import jwt, os
from models import User

def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            # split the token to get the actual token
            token = request.headers['Authorization']
            bearer = token.split()[0]
            token = token.split()[1]
        # return 401 if token is not passed
        if not token: return jsonify({ 'message': 'Token is missing' }), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            # fetch the user to whom the token belongs
            current_user = User.query.filter_by(username=data['user']).first()
            # returns the current logged in users contex to the routes
            return fn(current_user, *args, **kwargs)
        # throws exception if token is expired
        except jwt.ExpiredSignatureError:
            return jsonify({ 'message': 'Token has expired' }), 401
        # throws exception if token does not match
        except jwt.InvalidTokenError:
            return jsonify({ 'message': 'Invalid token' }), 401
        # return 401 if token is not passed
        except Exception as e:
            return jsonify({ 'message': 'Token is invalid' }), 401
    return decorated
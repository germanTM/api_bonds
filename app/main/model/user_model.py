from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ...main.schema.user_schema import Users
from ..error_handler import RaiseCustomException
import jwt
import uuid
from ... import app, db
import datetime

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            raise RaiseCustomException('A valid token is missing', 400)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            raise RaiseCustomException('Invalid token', 400)         
        return f(current_user, **kwargs)
    return decorator

"""Function to process the signing up of an user"""
def signup_user(user_data):
    if len(user_data['password']) not in range(8,30):
        raise RaiseCustomException('Password must have a length of between 8 and 30 characters', 400)

    if not user_data['name']:
        raise RaiseCustomException('The "name" field is missing', 400)
    hashed_password = generate_password_hash(user_data['password'], method='sha256')
    new_user = Users(public_id=str(uuid.uuid4()), name=user_data['name'], password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'registration complete'}, 201

"""Function to process the login of an user"""
def login_user(data):
    auth = data
    if not auth or not auth.username or not auth.password:
        raise RaiseCustomException('Missing some auth info', 400)

    user = Users.query.filter_by(name=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return {'message': 'Success processing the request','token': token.decode('UTF-8')}
    raise RaiseCustomException('Incorrect password', 400)

"""Function to gather user's data"""
def get_all_users():
    users = Users.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data['public_data'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password

        result.append(user_data)
    return {'message': 'Success processing the request', 'users': result}
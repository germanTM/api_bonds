from flask import request, abort
from ..util.dto import UserDto
from flask_restplus import Resource, api, fields
from ..error_handler import InvalidUserData
from ..model.user_model import signup_user, login_user, token_required, get_all_users

api = UserDto.api

@api.route("/login")
class BondPublications(Resource):
    login_request_fields = api.model('login_request', {
        'name': fields.String,
        'password': fields.String
    })

    login_response_fields = api.model('login_response', {
        'message': fields.String,
        'token': fields.String
    })

    @api.response(201, 'Success processing the request', login_response_fields)
    @api.doc('Login')
    @api.expect(login_request_fields)
    def post(self):
        """Login"""
        try:
            return login_user(request.authorization)
        except InvalidUserData as e:
            abort(e.status_code, e.message)

@api.route("/register")
class UserRegistration(Resource):
    register_request_fields = api.model('register_request', {
        'name': fields.String,
        'password': fields.String
    })

    register_response_fields = api.model('register_response', {
        'message': fields.String,
    })

    @api.response(201, 'Success processing the request', register_response_fields)
    @api.doc('Register user')
    @api.expect(register_request_fields)
    def post(self):
        """register user"""
        try:
            data = request.get_json()
            return signup_user(data)
        except Exception as e:
            print(e)
            abort(e.status_code, e.message)

@api.route("/listUsers")
class UserList(Resource):

    user_list_response_fields = api.model('user_list_response', {
        'message': fields.String,
        'users': fields.Arbitrary
    })

    @api.response(201, 'Success processing the request', user_list_response_fields)
    @api.doc('List users')
    @token_required
    def get(self):
        """user_list"""
        try:
            authUser = get_all_users()
            return authUser
        except Exception as e:
            abort(e)
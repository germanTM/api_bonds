from flask_restplus import Namespace

class UserDto:
    api = Namespace('user', description='Users related calls')

class BondDto:
    api = Namespace('bond', description='Users related calls')
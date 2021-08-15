from flask_restplus import Api
from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

db = SQLAlchemy(app)

blueprint = Blueprint('api', __name__)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["1000 per minute"])

api = Api(blueprint,
          title='FLASK EXCHANGE TRANSACTIONS API',
          version='1.0',
          description='An api to visualize info and make transactions between currencies'
          )

from .main.controller.user_controller import api as user_endpoint
from .main.controller.bond_controller import api as bond_endpoint

api.add_namespace(user_endpoint, path="/user")
api.add_namespace(bond_endpoint, path="/bond")

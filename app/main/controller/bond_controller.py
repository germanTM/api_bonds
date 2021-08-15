from flask import request, abort
from ..util.dto import BondDto
from flask_restplus import Resource, api, fields
from ...main.model.user_model import token_required
from ...main.model.bond_model import publish_bond, list_bonds, buy_bond, list_bonds_with_converted_price
from ... import limiter

api = BondDto.api

@api.route("/publishBond")
class BondPublications(Resource):
    publish_bond_request_fields = api.model('publish_bond_request', {
        'name': fields.String,
        'number': fields.Integer,
        'price': fields.Float
    })

    publish_bond_response_fields = api.model('publish_bond_response', {
        'message': fields.String
    })

    @token_required
    @api.response(201, 'Bonds were correctly published', publish_bond_response_fields)
    @api.doc('Publish bond')
    @api.expect(publish_bond_request_fields)
    @limiter.limit("1000/minute")
    def post(self):
        """Publish bond"""
        try:
            data = request.get_json()
            return publish_bond(self, data)
        except Exception as e:
            abort(e.status_code, e.message)

@api.route("/listBonds")
class BondList(Resource):

    list_bonds_response_fields = api.model('list_bonds_response', {
        'message': fields.String,
        'bonds': fields.Arbitrary
    })

    @token_required
    @api.response(201, 'Request proccessed successfully', list_bonds_response_fields)
    @api.doc('List all bonds')
    @limiter.limit("1000/minute")
    def get(self):
        """List all bonds"""
        try:
            return list_bonds()
        except Exception as e:
            print(e)
            abort(e.status_code, e.message)

@api.route("/listBonds/<currency>")
class BondListsDiverseCurrencies(Resource):

    list_bonds_response_fields = api.model('list_bonds_response', {
        'message': fields.String,
        'bonds': fields.Arbitrary
    })

    @token_required
    @api.response(201, 'Request proccessed successfully', list_bonds_response_fields)
    @api.doc('List all bonds based on a certain currency')
    @limiter.limit("1000/minute")
    def get(self, currency):
        """List all bonds based on a certain currency"""
        try:
            return list_bonds_with_converted_price(currency)
        except Exception as e:
            abort(e.status_code, e.message)


@api.route("/buyBond")
class BondSales(Resource):
    buy_bond_request_fields = api.model('buy_bond_request', {
        'bond_code': fields.String
    })

    buy_bond_response_fields = api.model('buy_bond_response', {
        'message': fields.String,
    })

    @token_required
    @api.response(201, 'Request proccessed successfully', buy_bond_response_fields)
    @api.doc('Buy bonds')
    @api.expect(buy_bond_request_fields)
    @limiter.limit("1000/minute")
    def post(self):
        """Buy bonds"""
        try:
            data = request.get_json()
            return buy_bond(self, data)
        except Exception as e:
            abort(e.status_code, e.message)
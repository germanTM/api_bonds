from ...main.schema.bond_schema import Bonds
from ...main.service.bond_service import get_mxn_usd_currency_exchange
from ...main import db
from ..error_handler import InvalidUserData
import uuid

def publish_bond(self, bond_data):
    if len(bond_data['name']) not in range(2,41):
        raise InvalidUserData('Name out of range', 400)

    if int(bond_data['number']) not in range(0,10000):
        raise InvalidUserData('Number of bonds must be a value between 1 and 10000', 400)

    if int(bond_data['price']) not in range(0,100000000):
        raise InvalidUserData('Total price must be a value between 0 and 100000000', 400)
    
    new_bond = Bonds(name=bond_data['name'], 
                    number=bond_data['number'], 
                    price=bond_data['price'], 
                    code=str(uuid.uuid4()),
                    seller=self.public_id
                )
    db.session.add(new_bond)
    db.session.commit()
    return {'message': "Bonds were correctly published"}, 201


def list_bonds():
    result = []
    bonds = Bonds.query.all()
    for bond in bonds:
        bond_data = {}
        bond_data['name'] = bond.name
        bond_data['number'] = bond.number
        bond_data['price'] = 'MXN ' + str(bond.price)
        bond_data['code'] = bond.code
        result.append(bond_data)
    return {'message':'Request proccessed successfully' ,'bonds': result} ,201

def buy_bond(self, request):
    bond_for_sale = Bonds.query.filter_by(code=request['bond_code']).first()
    if bond_for_sale:
        """Verify that the bonds are not linket to a buyer and that the user is not the owner of the bond"""
        if bond_for_sale.buyer == None and bond_for_sale.owner != self.public_id:
            bond_for_sale.buyer = self.public_id
            db.session.commit()
            return {'message': 'Request proccessed successfully'}, 201
        else:
            raise InvalidUserData('Either the bonds are owned by a buyer or the user is the owner ', 400)
    else:
        raise InvalidUserData('There are no bonds linked to the requested code', 400)

def list_bonds_with_converted_price(currency):
    result = []
    currency_methods = {
        'USD': get_mxn_to_usd_exchange_value()
    }
    requested_currency_value = currency_methods.get(currency, False)
    if requested_currency_value:
        bonds = Bonds.query.all()
        for bond in bonds:
            bond_data = {}
            bond_data['name'] = bond.name
            bond_data['number'] = bond.number
            bond_data['price'] = bond.price * float(requested_currency_value)
            bond_data['code'] = bond.code
            result.append(bond_data)
        return { 'message': 'Request proccessed successfully', 'bonds': result }, 201   
    else:
        raise InvalidUserData('Invalid currency', 400)

def get_mxn_to_usd_exchange_value():
    currency_value = 0
    usd_currency_data = get_mxn_usd_currency_exchange()
    if usd_currency_data['error']:
        raise InvalidUserData('Banxico responded with the following error: '+ usd_currency_data['error']['mensaje'], 400)
    currency_value = usd_currency_data['bmx']['series'][0]['datos'][0]['dato']
    if currency_value:
        return currency_value
    else:
        raise InvalidUserData('Banxico responded with incomplete data', 400)

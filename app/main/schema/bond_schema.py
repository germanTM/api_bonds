from ... import db

class Bonds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    number = db.Column(db.Integer)
    price = db.Column(db.Float)
    seller = db.Column(db.Integer, db.ForeignKey('users.public_id'))
    buyer = db.Column(db.Integer, db.ForeignKey('users.public_id'))
    code = db.Column(db.Integer)
    
def initialize_db():
    db.create_all()
    return 
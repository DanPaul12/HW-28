from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqlconnector://root:thegoblet2@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

#-------------------------------------------------------------------------------------

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (255), nullable = False)
    email = db.Column(db.String (320))
    phone = db.Column(db.String (15))
    orders = db.relationship('Orders', backref = 'customer')

class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (255), nullable = False)
    price = db.Column(db.Float, nullable = False)

class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    price = fields.String(required=True)

product_schema = CustomerSchema()
products_schema = CustomerSchema(many=True)

class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"))

class CustomerAcccount(db.Model):
    __tablename__ = 'CustomerAccount'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"))
    customer = db.relationship('Customer', backref = 'customer_account', uselist=False)


order_product = db.Table('Order_Product',
        db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key = True),
        db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key = True))


#-------------------------------------------------------------------------------------

@app.route('/customers', methods= ['POST'])
def add_customer():
    customer_data = customer_schema.load(request.json)
    if customer_data is None:
        return jsonify({'message':'customer not found'})
    customer = Customer(name = customer_data['name'], email = customer_data['email'], phone = customer_data['phone'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message':'customer added'}), 200


@app.route('/customers<int:id>', methods= ['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)


@app.route('/customers<int:id>', methods= ['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    customer_data = customer_schema.load(request.json)
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
    db.session.commit()
    return jsonify({"message":"member updated"}), 201

@app.route('/customers<int:id>', methods= ['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message":"member deleted"}), 201

#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
    

    
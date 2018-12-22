from ep_oms import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))

  def __repr__(self):
    return '<Admin {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password(self.password_hash, password)

@login.user_loader
def load_user(id):
  return Admin.query.get(int(id))

class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  email = db.Column(db.String(120), index=True, unique=True)
  name = db.Column(db.String(60))
  # Relationship: One-to-Many
  orders = db.relationship('Order', backref='customer', lazy='dynamic')

  def __repr__(self):
    return '<Customer ID: {} Email: {}>'.format(self.id, self.email)


class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  transit_days = db.Column(db.Integer)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
  to_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
  # Relationship: One-to-Many
  line_items = db.relationship('LineItem', backref='order', lazy='dynamic')
  # Relationship: One-to-One (Reference: https://stackoverflow.com/questions/3464443/sqlalchemy-one-to-one-db.relationship-with-declarative/9611874#9611874)
  shipment = db.relationship("Shipment", uselist=False, backref="order")

  def __repr__(self):
    return '<Order ID: {}>'.format(self.id)    


class Address(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  company = db.Column(db.String(30))
  name = db.Column(db.String(60))
  email = db.Column(db.String(60))
  street1 = db.Column(db.String(30))
  street2 = db.Column(db.String(30))
  street3 = db.Column(db.String(30))
  city = db.Column(db.String(30))
  state = db.Column(db.String(2))
  zip = db.Column(db.String(10))
  country = db.Column(db.String(2), default='US')
  residential = db.Column(db.Boolean())
  verified = db.Column(db.Boolean())
  ep_address_id = db.Column(db.String(30))
  # shipments = db.relationship('Shipment', backref='address', lazy='dynamic')

  def __repr__(self):
    return '<Address ID: {}>'.format(self.id)


class LineItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  quantity = db.Column(db.Integer)
  order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

  def __repr__(self):
    return '<LineItem ID: {}>'.format(self.id)


class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  sku = db.Column(db.String(30), unique=True)
  weight = db.Column(db.Integer)
  length = db.Column(db.Integer)
  width = db.Column(db.Integer)
  height = db.Column(db.Integer)
  description = db.Column(db.String(60))
  price = db.Column(db.Integer)
  ship_req_id = db.Column(db.Integer) # "Dummy" foreign key (TO DO: Create ShipReq table)
  # Relationship: One-to-Many
  line_items = db.relationship('LineItem', backref='product', lazy='dynamic')

  def __repr__(self):
    return '<Product ID: {}>'.format(self.id)


class Shipment(db.Model):
  __tablename__ = 'shipment'
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  to_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
  from_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
  parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.id'))
  order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
  carrier_id_1 = db.Column(db.Integer, db.ForeignKey('carrier.id')) # (TO DO: Manage Rates table)
  carrier_id_2 = db.Column(db.Integer, db.ForeignKey('carrier.id'))
  carrier_id_3 = db.Column(db.Integer, db.ForeignKey('carrier.id'))
  ship_req_id = db.Column(db.Integer) # "Dummy" foreign key (TO DO: Create ShipReq table)
  # Relationship: Many-to-One
  to_address = db.relationship("Address", foreign_keys=[to_address_id])
  from_address = db.relationship("Address", foreign_keys=[from_address_id])
  carrier_1 = db.relationship("Carrier", foreign_keys=[carrier_id_1])
  carrier_2 = db.relationship("Carrier", foreign_keys=[carrier_id_2])
  carrier_3 = db.relationship("Carrier", foreign_keys=[carrier_id_3])

  def __repr__(self):
    return '<Shipment ID: {}>'.format(self.id)

  def print_to_address(self):
    return self.to_address().ep_address_id


class Parcel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  max_weight = db.Column(db.Integer)
  length = db.Column(db.Integer)
  width = db.Column(db.Integer)
  height = db.Column(db.Integer)
  package_type = db.Column(db.String(30))
  # Relationships: One-to-Many
  shipments = db.relationship('Shipment', backref='parcel', lazy='dynamic')

  def __repr__(self):
    return '<Parcel ID: {} Max Wt: {}>'.format(self.id, self.max_weight)


class Carrier(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(30))
  created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  ep_carrier_id = db.Column(db.String(60))
  from_country = db.Column(db.String(30))
  from_state = db.Column(db.String(30))
  to_country = db.Column(db.String(30))
  to_state = db.Column(db.String(30))
  # Relationships One-to-Many
  # shipments = db.relationship('Shipment', backref='carrier', lazy='dynamic')

  def __repr__(self):
    return '<Carrier ID: {} Carrier Name: {}>'.format(self.id, self.name)
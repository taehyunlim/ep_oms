from ep_oms import application, db
from ep_oms.models import Address, Product, LineItem, Order, Parcel, Shipment, Carrier, Customer, Admin

@application.shell_context_processor
def make_shell_context():
  return { 'db': db, 'Address': Address, 'Product': Product, 'LineItem': LineItem, \
    'Order': Order, 'Parcel': Parcel, 'Shipment': Shipment, 'Carrier': Carrier, \
    'Customer': Customer, 'Admin': Admin}
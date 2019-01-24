from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ep_oms import application, db
from ep_oms.forms import AddressForm, LoginForm, SignupForm, AdminSettingsForm, ProductForm
from ep_oms.models import Admin, Address, LineItem, Product, Shipment, Parcel
# from ep_oms.api import ep_to_address


@application.route('/')
@application.route('/index')
@login_required
def index():
  addresses = Address.query.all()
  return render_template('index.html', title='EP_OMS', addresses=addresses)

@application.route('/order')
@login_required
def order():
  addresses = Address.query.all()
  line_items = LineItem.query.all()
  products = Product.query.all()
  parcels = Parcel.query.all()
  shipments = Shipment.query.all()
  address_form = AddressForm()
  return render_template('order.html', title="Create an order", addresses=addresses, line_items=line_items, products=products, address_form=address_form)

@application.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    # Authenticate
    user = Admin.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid Admin ID or PW')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    # Redirect to "next" page
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)

@application.route('/logout')
def logout():
  logout_user()
  flash('Successfully signed out')
  return redirect(url_for('index'))

@application.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = SignupForm()
  if form.validate_on_submit():
    user = Admin(username=form.username.data, email=form.email.data)
    user.set_password(form.pw.data)
    db.session.add(user)
    db.session.commit()
    flash('Registered successfully')
    return redirect(url_for('login'))
  return render_template('signup.html', title='Signup', form=form)

@application.route('/admin_settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
  form = AdminSettingsForm(current_user.email)
  if form.validate_on_submit():
    current_user.email = form.email.data
    db.session.commit()
    flash('Updated successfully')
    return redirect(url_for('admin_settings'))
  elif request.method == 'GET':
    form.email.data = current_user.email
  return render_template('admin_settings.html', title='Admin Settings', form=form)

@application.route('/address/new', methods=['GET', 'POST'])
@login_required
def address():
  addresses = Address.query.all()
  form = AddressForm()
  if form.validate_on_submit():
    # ep_address_id = ep_to_address(address)
    address = Address(
      name = form.name.data,
      email = form.email.data,
      street1 = form.street1.data,
      street2 = form.street2.data,
      street3 = form.street3.data,
      city = form.city.data,
      state = form.state.data,
      zip = form.zip.data
      # ep_address_id = ep_address_id
    )
    db.session.add(address)
    db.session.commit()
    flash("Address for {} successfully saved.".format(form.name.data))
    return redirect(url_for('address'))
  return render_template('address.html', title='Address', form=form, addresses=addresses)

@application.route('/address/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_address(id):
  existing_addr = Address.query.filter_by(id=id).first()
  if existing_addr is None:
      flash('The address does not exist.')
      return redirect(url_for('address'))
  form = AddressForm()
  if form.validate_on_submit():
    existing_addr.email = form.email.data
    existing_addr.name = form.name.data
    existing_addr.street1 = form.street1.data
    existing_addr.street2 = form.street2.data
    existing_addr.street3 = form.street3.data
    existing_addr.city = form.city.data
    existing_addr.state = form.state.data
    existing_addr.zip = form.zip.data
    db.session.commit()
    flash("Successfully updated.")
    return redirect(url_for('address'))
  elif request.method == 'GET':
    form.email.data = existing_addr.email
    form.name.data = existing_addr.name
    form.street1.data = existing_addr.street1
    form.street2.data = existing_addr.street2
    form.street3.data = existing_addr.street3
    form.city.data = existing_addr.city
    form.state.data = existing_addr.state
    form.zip.data = existing_addr.zip
  return render_template('edit_address.html', title='Address', form=form)

@application.route('/product/new', methods=['GET', 'POST'])
@login_required
def product():
  products = Product.query.all()
  form = ProductForm()
  if form.validate_on_submit():
    product = Product(
      sku = form.sku.data,
      description = form.description.data,
      weight = form.weight.data,
      length = form.length.data,
      width = form.width.data,
      height = form.height.data,
      price = form.price.data,
    )
    db.session.add(product)
    db.session.commit()
    flash("Product (SKU: {}) successfully saved.".format(form.sku.data))
    return redirect(url_for('product'))
  return render_template('product.html', title='Product', form=form, products=products)

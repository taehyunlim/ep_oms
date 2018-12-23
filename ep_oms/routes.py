from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ep_oms import application, db
from ep_oms.forms import AddressForm, LoginForm, SignupForm, AdminSettingsForm
from ep_oms.models import Admin, Address


@application.route('/')
@application.route('/index')
@login_required
def index():
  addresses = Address.query.all()
  return render_template('index.html', title='EP_OMS', addresses=addresses)

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

@application.route('/_admin_settings', methods=['GET', 'POST'])
@login_required
def _admin_settings():
  form = AdminSettingsForm(current_user.email)
  if form.validate_on_submit():
    current_user.email = form.email.data
    db.session.commit()
    flash('Updated successfully')
    return redirect(url_for('_admin_settings'))
  elif request.method == 'GET':
    form.email.data = current_user.email
  return render_template('_admin_settings.html', title='Admin Settings', form=form)

@application.route('/address', methods=['GET', 'POST'])
@login_required
def address():
  form = AddressForm()
  if form.validate_on_submit():
    address = Address(
      name = form.name.data,
      email = form.email.data,
      street1 = form.street1.data,
      street2 = form.street2.data,
      street3 = form.street3.data,
      city = form.city.data,
      state = form.state.data,
      zip = form.zip.data
    )
    db.session.add(address)
    db.session.commit()
    flash("Address for {} successfully saved".format(form.name.data))
    return redirect(url_for('index'))
  return render_template('address.html', title='Address', form=form)
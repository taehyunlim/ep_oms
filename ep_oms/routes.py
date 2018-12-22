from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from ep_oms import application
from ep_oms.forms import AddressForm, LoginForm
from ep_oms.models import Admin


@application.route('/')
@application.route('/index')
def index():
  order = [{'id': 1, 'name': 'TL'}, {'id': 2, 'name': 'BT'}]
  return render_template('index.html', title='EP_OMS', order=order)

@application.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = Admin.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid Admin ID or PW')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign In', form=form)

@application.route('/logout')
def logout():
  logout_user()
  flash('Successfully signed out')
  return redirect(url_for('index'))

@application.route('/address', methods=['GET', 'POST'])
def address():
  form = AddressForm()
  if form.validate_on_submit():
    flash(form.email.data)
    return redirect(url_for('address'))
  return render_template('address.html', title='Address', form=form)
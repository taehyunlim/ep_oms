from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ep_oms import application, db
from ep_oms.forms import AddressForm, LoginForm, SignupForm
from ep_oms.models import Admin


@application.route('/')
@application.route('/index')
@login_required
def index():
  order = [{'id': 1, 'name': 'TL'}, {'id': 2, 'name': 'BT'}]
  return render_template('index.html', title='EP_OMS', order=order)

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
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = SignupForm()
  if form.validate_on_submit():
    user = Admin(username=form.username.data, email=form.email.data)
    user.set_password(form.pw.data)
    db.session.add(user)
    db.session.commit()
    flash('Success')
    return redirect(url_for('login'))
  return render_template('signup.html', title='Signup', form=form)

@application.route('/address', methods=['GET', 'POST'])
@login_required
def address():
  form = AddressForm()
  if form.validate_on_submit():
    flash(form.email.data)
    return redirect(url_for('address'))
  return render_template('address.html', title='Address', form=form)
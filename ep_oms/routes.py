from flask import render_template, flash, redirect, url_for
from ep_oms import application
from ep_oms.forms import AddressForm


@application.route('/')
@application.route('/index')
def index():
  order = [{'id': 1, 'name': 'TL'}, {'id': 2, 'name': 'BT'}]
  return render_template('index.html', title='EP_OMS', order=order)

@application.route('/address', methods=['GET', 'POST'])
def address():
  form = AddressForm()
  if form.validate_on_submit():
    flash(form.email.data)
    return redirect(url_for('address'))
  return render_template('address.html', title='Address', form=form)
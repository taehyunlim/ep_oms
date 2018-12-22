from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from ep_oms.models import Admin, Product

class LoginForm(FlaskForm):
  username = StringField('Admin ID', validators=[DataRequired()])
  password = PasswordField('PW', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
  username = StringField('Choose an Admin ID', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  pw = PasswordField('Password', validators=[DataRequired()])
  pw2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('pw', message='Repeated password did not match')])
  submit = SubmitField('Register')

  # Custom validator pattern: validate_<field_name>
  def validate_username(self, username):
    user_by_username = Admin.query.filter_by(username=username.data).first()
    if user_by_username is not None:
      raise ValidationError('Please use a different Admin ID')
  
  def validate_email(self, email):
    user_by_email = Admin.query.filter_by(email=email.data).first()
    if user_by_email is not None:
      raise ValidationError('Please use a different email address')

class AddressForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  name = StringField('Name', validators=[DataRequired()])
  # street1 = StringField('Street 1', validators=[DataRequired(), Length(min=0, max=30)])
  # street2 = StringField('Street 2', validators=[Length(min=0, max=30)])
  # street3 = StringField('Street 3', validators=[Length(min=0, max=30)])
  # city = StringField('City', validators=[DataRequired(), Length(min=0, max=30)])
  # state = StringField('State', validators=[DataRequired(), Length(min=0, max=2)])
  # zip = StringField('Zip', validators=[DataRequired(), Length(min=0, max=10)])
  submit = SubmitField('Save')

class ProductForm(FlaskForm):
  sku = StringField('SKU', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired()])
  weight = FloatField('Weight', validators=[DataRequired(), NumberRange(0,100)])
  length = FloatField('Length', validators=[DataRequired(), NumberRange(0,100)])
  width = FloatField('Width', validators=[DataRequired(), NumberRange(0,100)])
  height = FloatField('Height', validators=[DataRequired(), NumberRange(0,100)])
  price = FloatField('Price', validators=[DataRequired(), NumberRange(0,100)])
  submitProduct = SubmitField('Save')

  def validate_sku(self, sku):
    product = Product.query.filter_by(sku=self.sku.data).first()
    if product is not None:
      raise ValidationError("Duplicate SKU")
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_bootstrap import Bootstrap

# Main application instance
application = Flask(__name__)
application.config.from_object(Config)
# Flask-SQLAlchemy
db = SQLAlchemy(application)
migrate = Migrate(application, db)
# Flask-Login
login = LoginManager(application)
login.login_view = 'login'
# Flask-Bootstrap
bootstrap = Bootstrap(application)

# Import modules 
from ep_oms import routes, models, errors

# Error Logging: Email
if not application.debug and not application.testing:
  # Only enable email logger if the email server configs info exists
  # TEST: (venv) python -m smtpd -n -c DebuggingServer localhost:8025
  if application.config['MAIL_SERVER']:
    auth = None
    if application.config['MAIL_USERNAME'] or application.config['MAIL_PASSWORD']:
      auth = (application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD'])
    secure = None
    if application.config['MAIL_USE_TLS']:
      secure = ()
    mail_handler = SMTPHandler(
      mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
      fromaddr='no-reply@' + application.config['MAIL_SERVER'],
      toaddrs=application.config['ADMINS'], subject='EP_OMS Failure',
      credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    application.logger.addHandler(mail_handler)

# Error Logging: Local file output
if not application.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/ep_oms.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)

    application.logger.setLevel(logging.INFO)
    application.logger.info('EP_OMS Error Logging')
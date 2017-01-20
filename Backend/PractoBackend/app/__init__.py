from database import init_db, db_session
from flask import Flask
from flask.ext.admin import Admin
init_db()

app = Flask('app')
admin=Admin(app)														#used for admin interface.
from app import models, routes

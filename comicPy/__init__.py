"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comicPy.db'
app.config['SQLALCHEMY_BINDS'] = {'mylar': 'sqlite:///mylar.db'}
#app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/customlogin.html'

from comicPy.models import db

db.init_app(app)

import comicPy.routes












from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os

app = Flask(__name__)
app.secret_key = '@k//csac3432Jdjfh@cnsa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@pgdb:5432/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = os.environ['CACHE_TYPE']
app.config['CACHE_REDIS_HOST'] = os.environ['CACHE_REDIS_HOST']
app.config['CACHE_REDIS_PORT'] = os.environ['CACHE_REDIS_PORT']
app.config['CACHE_REDIS_DB'] = os.environ['CACHE_REDIS_DB']
app.config['CACHE_REDIS_URL'] = os.environ['CACHE_REDIS_URL']
app.config['CACHE_DEFAULT_TIMEOUT'] = os.environ['CACHE_DEFAULT_TIMEOUT']

db = SQLAlchemy(app)
cache = Cache(app)

from webapp import api

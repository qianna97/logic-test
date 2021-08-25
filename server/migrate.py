from app import db
from model import *

db.drop_all()
db.create_all()
db.session.commit()

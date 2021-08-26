from webapp import db 
import hashlib
import re
import random
import string
import datetime
from functools import wraps

def generateRefCode():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7)) 

def validate(func):
    def wrapper(*args, **kwargs):
        if all(k in kwargs for k in ("username","password","name","email")):
            kwargs['password'] = hashlib.sha3_256(kwargs['password'].encode()).hexdigest()
            
            if User.query.filter(User.username == kwargs['username']).first():
                raise AssertionError('Username is already in use')
            if re.match("^[a-zA-Z0-9]*$", kwargs['username']) is None:
                raise AssertionError('Username must be alphanumeric character')
            
            if not re.match("[^@]+@[^@]+\.[^@]+", kwargs['email']):
                raise AssertionError('Provided email is not an email address')
            if User.query.filter(User.email == kwargs['email']).first():
                raise AssertionError('Email is already in use')

            if re.match("^[a-zA-Z0-9]*$", kwargs['name']) is None:
                raise AssertionError('name must be alphanumeric character')
        
            return func(*args, **kwargs)
        else:
            raise AssertionError("Please fill the fields")
    return wrapper

class User(db.Model):
    __tabelname__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    refcode = db.Column(db.String(255), unique=True, default=generateRefCode())
   
    @validate
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @validate
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'username': self.username,
                'email': self.email
                }

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.name}')"

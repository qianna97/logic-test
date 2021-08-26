from flask import Blueprint, request, jsonify, make_response
from flask_restx import Api, Resource
from webapp.model import User
from webapp import app, cache
import hashlib
from functools import wraps
import jwt
import datetime
import requests

def encode_auth(id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        print(str(e))
        return None

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            auth_header = request.headers['Authorization']
        except KeyError:
            return make_response(jsonify(message='Login Required'), 401)
        if auth_header:
            try:
                payload = jwt.decode(auth_header, app.config.get('SECRET_KEY'), algorithms='HS256')
                user = User.query.filter_by(id=payload['sub']).first()
                if user:
                    return f(user, *args, **kwargs)
                else:
                    return make_response(jsonify(message='Invalid token'), 401)
            except Exception as e:
                return make_response(jsonify(message=str(e)), 401)
        else:
            return make_response(jsonify(message="Login Requiered"), 401)
    return decorator


authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(app,authorizations=authorizations)

@api.route('/registration')
@api.doc(params={'username': 'Username, alphanumeric, unique', 'password': 'Password for user', 'name': 'Name, alphanumeric', 'email': 'Valid Email'})
class Registration(Resource):
    def post(self):
        try:
            u = User(
                    username=request.args.get('username'),
                    password=request.args.get('password'),
                    name=request.args.get('name'),
                    email=request.args.get('email')
                    )
            u.save()
            return make_response(jsonify(message="User created"), 200)
        except Exception as e:
            return make_response(jsonify(message=str(e)), 400)

@api.route('/login')
@api.doc(params={'username': 'Username for login', 'password': 'Password user'})
class Login(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')

        if username is None or password is None:
            return make_response(jsonify(message="Please input username and password"), 400)

        hash_pw = hashlib.sha3_256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == hash_pw:
                auth_token = encode_auth(user.id)
                print(user.id)
                if auth_token is not None:
                    return make_response(jsonify(
                            token=auth_token,
                            username=user.username,
                            name=user.name,
                            email=user.email
                        ), 200)
                else:
                    return make_response(jsonify(message="Erorr creating token"), 401)
            else:
                return make_response(jsonify(message="Invalid credentials"), 401)
        else:
            return make_response(jsonify(message="User doesn't exist"), 401)

@api.route('/edit')
@api.doc(params={'username': 'Username, alphanumeric, unique', 'password': 'Password for user', 'name': 'Name, alphanumeric', 'email': 'Valid Email'})
class EditData(Resource):
    decorators = [auth_required]
    @api.doc(security='jwt')
    def put(self, current):
        u = User.query.filter_by(id=current.id).first()
        u.update(**request.args.to_dict())
        u.save()
        return make_response(jsonify(message="Update data success"), 200)
        

@api.route('/refcode')
@api.doc(params={'refcode': 'Ref Code'})
class Refcode(Resource):
    decorators = [auth_required]
    @api.doc(security='jwt')
    def post(self, current):
        refcode = request.args.get('refcode')
        if refcode:
            u = User.query.filter_by(refcode=refcode).first()
            if u and u.id != current.id:
                return make_response(jsonify(message="Success"), 200)
            else:
                return make_response(jsonify(message="Invalid Ref Code"), 400)
        return make_response(jsonify(message="Please input ref code"), 400)

@api.route('/find-user')
@api.doc(params={'name': 'Name User to looking for'})
class FindUser(Resource):
    def post(self):
        name = request.args.get('name')
        u = User.query.filter(User.name.like('%'+name+'%')).all()
        if u:
            return make_response(jsonify(data=[x.serialize for x in u]), 200)
        return make_response(jsonify(message="No user found"), 200)

@api.route('/get-hero')
@api.doc(params={'name': 'Name of hero LoL'})
class GetHero(Resource):
    @cache.cached(timeout=30, query_string=True)
    def post(self):
        name = request.args.get('name')
        req = requests.get(
                'https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'
                ).json()['data']
        for key, value in req.items():
            if name in key:
               return make_response(jsonify(req[key]), 200)
        return make_response(jsonify(message="Hero not found"), 200)

import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret1234'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
# api.add_resource(UserList, '/users')

api.add_resource(UserRegister, '/register')


# noinspection PyUnusedLocal
@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization Header'}), 401


# @app.route('/')
# def home():
#     return "Automate Testing Course Test REST API 2"


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

    if app.config['DEBUG']:
        @app.before_request
        def create_tables():
            db.create_all()

    app.run(port=5000)

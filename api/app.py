'''packages and library import'''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from flask_restful import Resource, Api

'''database connection'''
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{username}:{password}}@{host}:5432/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app) # to work with json responses


'''User Class to auto create the user table'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32),unique = True)
    password = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    age = db.Column(db.Integer)

    def __init__(self, username, password, first_name, last_name, age):
        self.usename = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

'''user schema'''
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'age')


'''declare user schema'''
# signle user
user_schema = UserSchema()
# multiple users
users_schema = UserSchema(many = True)

'''API'''
class UserManager(Resource):
    pass

    '''GET()'''
    @staticmethod
    def get():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            users = User.query.all()
            return jsonify(user_schema.dump(users))
        user = User.query.get(id)
        return jsonify(user_schema.dump(uer))

    @staticmethod
    def post():
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        age = request.json['age']

        user = User(username, password, first_name, last_name, age)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {first_name}, {last_name} inserted.'
        })

    '''Update a signal user'''
    @staticmethod
    def put():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            return jsonify({'Message': 'Must provide the user ID' })
            
            user = User.query.get(id)
            username = request.json['username']
            password = request.json['password']
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            ago = request.json['age']

            user.username = username
            user.password = password
            user.fist_name = first_name
            user.last_name = last_name
            user.age = age

            db.session.commit()
            return jsonify({
                'Message': f'User {first_name} {last_name} altered.'
            })


    '''delete a user'''
    @staticmethod
    def delete():
        try: id = request.args['id']
        except Exception as _: id = None
        
        if not id:
            return jsonify({'Message': ' Must provide the user ID'})

        user = User.query.get(id)
        db.sessio.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(id)} deleted.'
        })

api.add_resource(UserManager, '/api/users')

if __name__=='__main__':
    app.run(debug = True)

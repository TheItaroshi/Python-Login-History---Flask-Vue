from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_restplus import Api
from datetime import datetime, timezone, timedelta
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_new.db'
api = Api(app)
db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)
CORS(app)
JWTManager(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'FC01D1F2EA853CE3E6995DF1DF50C0DA0E618369B1EE8078202C630376577109'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    token = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.surname}', '{self.username}', '{self.password}', '{self.token}')"


class LoginDateTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Login date('{self.login_date}')"


db.init_app(app)


@app.route('/home', methods=["POST"])
def create_entry():
    req = request.get_json()
    username = req.get('username')
    password = req.get('password')
    resp = ''
    try:

        username_check = username == User.query.filter_by(username=username).first().username
        password_check = flask_bcrypt.check_password_hash(User.query.filter_by(username=username).first().password, password.encode('utf-8'))

        if username_check and password_check:
            access_token = User.query.filter_by(username=username).first().token
            resp = {'token': access_token}

    except:

        resp = {'status': 'nok'}

    return resp


@app.route('/history', methods=["POST"])
@cross_origin()
def show():
    req = request.get_json()
    try:
        token = req.get('token')
        user_id = User.query.filter_by(token=token).first().id
        log = LoginDateTime(login_date=datetime.now(timezone(timedelta(hours=2))), user_id=user_id)
        db.session.add(log)
        db.session.commit()
        print(req)
        print(LoginDateTime.query.all())
        resp = []

        for row in LoginDateTime.query.all():
            if row.user_id == user_id:
                info = {
                    'name': User.query.filter_by(id=user_id).first().name,
                    'surname': User.query.filter_by(id=user_id).first().surname,
                    'date': row.login_date
                }
                print(info)
                resp.append(info)
        print(resp)
    except:
        resp = {'error': 'wrong token'}
    return jsonify(resp)

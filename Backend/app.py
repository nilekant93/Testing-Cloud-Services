from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from flask import request, jsonify
from dotenv import load_dotenv
load_dotenv()  # lataa .env-tiedoston muuttujat ympäristöön
import os

app = Flask(__name__, instance_relative_config=True)
CORS(app)

# Luo 'instance' -kansio tarvittaessa
os.makedirs(app.instance_path, exist_ok=True)

# Tietokannan asetukset
db_path = os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'salainen_avain'

db.init_app(app)
jwt = JWTManager(app)


@app.route('/ping')
def ping():
    return jsonify({'message': 'pong'}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    class_code = data.get('class_code')

    if not username or not password or not class_code:
        return jsonify({'error': 'Kaikki kentät ovat pakollisia'}), 400

    if not username.isalnum() or not class_code.isalnum():
        return jsonify({'error': 'Vain kirjaimia ja numeroita sallittu'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Käyttäjänimi on jo olemassa'}), 409

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        class_code=class_code
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Käyttäjä luotu onnistuneesti'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Wrong password or username'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'token': token, 'class_code': user.class_code}), 200

@app.route('/users')
def list_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'class_code': user.class_code
        })
    return jsonify(result)

# Vain ensimmäisellä kerralla luodaan tietokanta


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=3001, debug=True)

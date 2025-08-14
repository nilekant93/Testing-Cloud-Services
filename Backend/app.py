from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from flask import request, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt_identity
load_dotenv()  
import os

import Week1
import Week3
import Week3_1


ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

app = Flask(__name__, instance_relative_config=True)
CORS(app)

os.makedirs(app.instance_path, exist_ok=True)

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
        return jsonify({'error': 'All fields are required'}), 400

    if not username.isalnum() or not class_code.isalnum():
        return jsonify({'error': 'Only letters and numbers are allowed'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'username already exists'}), 409

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        class_code=class_code
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

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

# Admin login endpoint

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        token = create_access_token(identity='admin')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # käyttäjien haku admin sovellukseen
@app.route('/admin/users', methods=['GET'])
def admin_get_users():
    users = User.query.all()
    result = []

    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'class_code': user.class_code,
            'week1': user.week1done,
            'week2': user.week2done,
            'week3': user.week3done,
            'week4': user.week4done,
            'week5': user.week5done,
        })

    return jsonify(result), 200

# käyttäjän poisto tietokannasta
@app.route('/admin/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

#Lisätään kantaan "tehty" arvo
@app.route('/mark_week_done', methods=['POST'])
@jwt_required()
def mark_week_done():
    data = request.get_json()
    week_key = data.get('week')  

    if week_key not in ['week1done', 'week2done', 'week3done', 'week4done', 'week5done']:
        return jsonify({'error': 'Invalid week key'}), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    setattr(user, week_key, True)
    db.session.commit()

    return jsonify({'message': f'{week_key} marked as done'}), 200

#haetaan kirjautumisen jälkeen jo tehdyt testit
@app.route('/user/progress', methods=['GET'])
@jwt_required()
def get_user_progress():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    progress = {
        'week1Tested': user.week1done,
        'week2Tested': user.week2done,
        'week3Tested': user.week3done,
        'week4Tested': user.week4done,
        'week5Tested': user.week5done,
    }

    return jsonify(progress), 200



# TESTIEN SUORITTAMINEN


@app.route('/receive', methods=['POST'])
@jwt_required()
def receive():
    data = request.get_json()
    component = data.get('component', 'Unknown')
    lesson_key = data.get('lesson')
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    print(f"Received data from user: {user.username}, component: {component}")

    if component == 'Week1':
        url = data.get('url')
        result, checks = Week1.run_test(url, user.username)
        return jsonify({
            'status': 'success',
            'test_passed': result,
            'checks': checks
        }), 200
        
    elif component == 'Week2':
        url = data.get('url')
        import Week2  # varmista että Week2.py on backendin juuressa
        result, checks = Week2.run_test(url, user.username)

        # jos testi menee läpi, merkitään kantaan tehdyksi
        if result:
            user.week2done = True
            db.session.commit()

        return jsonify({
            'status': 'success',
            'test_passed': result,
            'checks': checks
        }), 200


    elif component == 'Week3':
        url = data.get('url')
        if lesson_key == 'lesson2':
            result, message = Week3_1.run_test(url, user.username)
        else:
            result, message = Week3.run_test(url, user.username)
        return jsonify({
            'status': 'success',
            'test_passed': result,
            'message': message if isinstance(message, str) else '',
            'checks': message if isinstance(message, list) else []
        }), 200

    elif component == 'Week4':
        url = data.get('url')
        import Week4
        result, checks = Week4.run_test(url, user.username)
        return jsonify({
            'status': 'success',
            'test_passed': result,
            'checks': checks
        }), 200

    elif component == 'Week5':
        site_url = data.get('siteUrl')
        readme_url = data.get('readmeUrl')
        if not site_url or not readme_url:
            return jsonify({'error': 'Both siteUrl and readmeUrl are required for Week5'}), 400
        
        import Week5 
        result, checks = Week5.run_test(site_url, readme_url, user.username)
        
        if result:
            user.week5done = True
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'test_passed': result,
            'checks': checks
        }), 200

    else:
        return jsonify({'status': 'unknown component'}), 400




# Vain ensimmäisellä kerralla luodaan tietokanta


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=3001, debug=True)

# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    class_code = db.Column(db.String(20), nullable=False)
    
    week1done = db.Column(db.Boolean, default=False, nullable=False)
    week2done = db.Column(db.Boolean, default=False, nullable=False)
    week3done = db.Column(db.Boolean, default=False, nullable=False)
    week4done = db.Column(db.Boolean, default=False, nullable=False)
    week5done = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
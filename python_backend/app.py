from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40ck159357@localhost/vocabularydb'
db = SQLAlchemy(app)


class Word(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # 修改为字符串格式以存储UUID
    word = db.Column(db.String(255), unique=True, nullable=False)
    definition = db.Column(db.String(255), nullable=False)
    example = db.Column(db.String(255), nullable=False)
    example_translation = db.Column(db.String(255), nullable=True)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expiry = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def check_password(self, password):
        return check_password_hash(self._password, password)

class UserWord(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    word_id = db.Column(db.String(36), db.ForeignKey('word.id'))
    status = db.Column(db.String(10), nullable=False, default='active')

    user = db.relationship('User', backref=db.backref('userwords', lazy=True))
    word = db.relationship('Word', backref=db.backref('userwords', lazy=True))

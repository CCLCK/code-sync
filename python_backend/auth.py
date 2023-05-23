from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from app import app,db,User
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import random
from flask_cors import CORS
import os

CORS(app)
smtp_server = 'smtp.qq.com'
from_addr = '1946605630@qq.com'
password = 'fclwiymyqesrbebi'

def send_verification_code(email):
    user = get_user_by_email(email)
    verification_code = str(random.randint(100000, 999999))
    print(verification_code)
    user.verification_code = verification_code
    user.verification_code_expiry = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()

    content = '''Hello,

Thank you for registering at Word Journeyman.

Your verification code is: {}

Please enter this code on the Word Journeyman website to complete your registration.

If you did not request this code, please ignore this email.

Best regards,
The Word Journeyman Team
'''.format(verification_code)

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = 'Word Journeyman Registration Verification Code'
    msg['From'] = from_addr
    msg['To'] = email

    server = smtplib.SMTP_SSL(smtp_server)
    server.login(from_addr, password)
    server.sendmail(from_addr, [email], msg.as_string())
    server.quit()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def handle_verification(email):
    try:
        send_verification_code(email)
    except Exception as e:
        raise ValueError("An error occurred while sending the verification code: " + str(e))

def register_user(email, password):
    user = get_user_by_email(email)

    if user:
        print(user)
        raise ValueError("Email already registered")
    else:
        hashed_password = generate_password_hash(password, method='MD5')
        user = User(
            id=str(uuid4()),
            email=email,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        return user


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(email)
    print(password)
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    try:

        user = register_user(email, password)

        handle_verification(email)

        return jsonify({'message': 'Verification code sent'}), 200
    except ValueError as e:

        return jsonify({'message': str(e)}), 400

@app.route('/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        email = data.get('email')
        verification_code = data.get('verification_code')
        if not email or not verification_code:
            return jsonify({'message': 'Email and verification code are required'}), 400
        user = get_user_by_email(email)
        if verification_code != user.verification_code or datetime.utcnow() > user.verification_code_expiry:
            return jsonify({'message': 'Invalid or expired verification code'}), 400
        user.verification_code = None
        user.verification_code_expiry = None
        user.is_active = True
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = get_user_by_email(email)
        print(password)

        if not user.is_active:
            return jsonify({'message': 'Please verify your email before logging in'}), 400
        if not user.check_password(password):
            return jsonify({'message': 'Invalid email or password'}), 400

        # Logged in successfully, return user id
        return jsonify({'message': 'Logged in successfully', 'user_id': user.id}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5400)
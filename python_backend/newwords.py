from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app import UserWord, User, Word,app,db
from uuid import uuid4
import os

CORS(app)
@app.route('/api/user/add_word', methods=['POST'])
def add_word():
    data = request.get_json()
    user_id = data.get('user_id')
    word_text = data.get('word')

    word = Word.query.filter_by(word=word_text).first()
    if not word:
        return jsonify({'status': 'error', 'message': 'Word not found'}), 400

    new_user_word = UserWord(id=str(uuid4()), user_id=user_id, word_id=word.id)
    db.session.add(new_user_word)
    db.session.commit()

    return jsonify({'status': 'success'}), 200


@app.route('/api/user/remove_word', methods=['POST'])
def remove_word():
    data = request.get_json()
    user_id = data.get('user_id')
    word_text = data.get('word')

    word = Word.query.filter_by(word=word_text).first()
    if not word:
        return jsonify({'status': 'error', 'message': 'Word not found'}), 400

    user_word = UserWord.query.filter_by(user_id=user_id, word_id=word.id).first()
    if user_word:
        db.session.delete(user_word)
        db.session.commit()

    return jsonify({'status': 'success'}), 200


@app.route('/api/user/words', methods=['GET'])
def get_words():
    user_id = request.args.get('user_id')

    words = Word.query.join(UserWord, UserWord.word_id == Word.id).filter(UserWord.user_id == user_id).all()
    print(words)
    return jsonify({'status': 'success', 'words': [word.word for word in words]}), 200


if __name__ == "__main__":
    app.run(port=5500)

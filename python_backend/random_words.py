from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40ck159357@localhost/VocabularyDB'
db = SQLAlchemy(app)
CORS(app)

class Word(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    word = db.Column(db.String(255), unique=True, nullable=False)
    definition = db.Column(db.String(255), nullable=False)
    example = db.Column(db.String(255), nullable=False)
    example_translation = db.Column(db.String(255), nullable=True)

@app.route('/random-words', methods=['GET'])
def get_random_words():
    all_words = Word.query.filter(Word.example != "").all()
    random_sample = random.sample(all_words, 10)
    return jsonify([{
        "word": word.word,
        "definition": word.definition,
        "example": word.example,
        "example_translation": word.example_translation
    } for word in random_sample])

if __name__ == '__main__':
    app.run(port=5300, debug=True)

from flask import Flask, jsonify, abort, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40ck159357@localhost/VocabularyDB'
db = SQLAlchemy(app)
CORS(app)

class Word(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # 修改为字符串格式以存储UUID
    word = db.Column(db.String(255), unique=True, nullable=False)
    definition = db.Column(db.String(255), nullable=False)
    example = db.Column(db.String(255), nullable=False)
    example_translation = db.Column(db.String(255), nullable=True)

@app.route('/words/<word>', methods=['GET'])
def get_word(word):
    word_object = Word.query.filter_by(word=word).first()
    if word_object is None:
        abort(404)
    return jsonify({
        "word": word_object.word,
        "definition": word_object.definition,
        "example": word_object.example,
        "example_translation": word_object.example_translation
    })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Word not found'}), 404)

if __name__ == '__main__':
    app.run(port=5100,debug=True)

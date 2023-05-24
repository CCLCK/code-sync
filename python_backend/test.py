import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import Word,app



@app.route('/test_db', methods=['GET'])
def test_db():
    # Attempt to fetch one word from the database
    word = Word.query.first()

    if word is None:
        return "No words found. Database seems to be empty.", 200
    else:
        return f"Word found: {word.word}", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
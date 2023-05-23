import uuid
import re
import time
import concurrent.futures
import bs4
import requests
import nltk
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.ddl import DropTable
from app import Word
# 初始化Flask应用和数据库
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40ck159357@localhost/vocabularydb'
db = SQLAlchemy(app)

# 定义数据库模型

# 创建应用上下文
with app.app_context():
    # 创建数据库表
    db.create_all()

    # 获取单词列表
    nltk.download('words')
    from nltk.corpus import words
    word_list = words.words()

    # 初始化已经插入的单词集合
    inserted_words = {word.word for word in Word.query.all()}


    def process_word(word_to_scrape):
        with app.app_context():
            try:
                url = f'https://corp.dict.cn/search?q={word_to_scrape}'
                print(url)
                response = requests.get(url)

                soup = BeautifulSoup(response.text, 'html.parser')
                word_meaning_ul = soup.find('ul', class_='dict-basic-ul')
                if word_meaning_ul is None:
                    return
                word_meaning = word_meaning_ul.find('strong').text
                print("单词意思:", word_meaning)

                english_sentence = ''
                chinese_sentence = ''

                div = soup.find('div', {'class': 'layout sort'})
                if div is not None:
                    li = div.find('ol').find('li')
                    text = li.get_text()
                    match = re.search('[\u4e00-\u9fff]', text)
                    if match:
                        chinese_start = match.start()
                        english_sentence = text[:chinese_start].strip()
                        chinese_sentence = text[chinese_start:].strip()

                if word_to_scrape not in inserted_words:
                    new_word = Word(id=str(uuid.uuid4()), word=word_to_scrape,
                                    definition=word_meaning,
                                    example=english_sentence,
                                    example_translation=chinese_sentence)
                    db.session.add(new_word)
                    inserted_words.add(word_to_scrape)
                    db.session.commit()
                else:
                    existing_word = Word.query.filter_by(word=word_to_scrape).first()
                    existing_word.definition = word_meaning
                    existing_word.example = english_sentence
                    existing_word.example_translation = chinese_sentence
                    db.session.commit()
            except Exception as e:
                print(f"Error processing word {word_to_scrape}: {e}")


    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        list(executor.map(process_word, word_list))

    # 最后一次提交数据库会话
    db.session.commit()

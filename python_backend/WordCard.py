from flask import Flask, jsonify, abort

app = Flask(__name__)

# 假设你有一个词汇数据库，这里我们只是用一个简单的列表来模拟
words = [
    {"word": "apple", "definition": "一种常见的水果"},
    {"word": "banana", "definition": "一种常见的黄色水果"},
    # ...其他单词
]


# 创建一个动态路由
@app.route('/words/<word>', methods=['GET'])
def get_word(word):
    # 在你的词汇数据库中查找这个单词
    word_object = next((w for w in words if w["word"] == word), None)

    if word_object is None:
        abort(404)  # 如果没有找到单词，返回404错误

    return jsonify(word_object)  # 如果找到了单词，返回单词的JSON表示


if __name__ == '__main__':
    app.run(debug=True)

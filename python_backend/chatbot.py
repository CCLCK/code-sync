from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(24)

# 设置你的 OpenAI 密钥
openai.api_key = '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'


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message_input = data.get('message')

    if 'messages' not in session:
        session['messages'] = []

    session['messages'].append({"role": "user", "content": message_input})

    messages_to_send = [
                           {"role": "system", "content": """
          作为一位经验丰富且知识深厚的英语教师，你拥有深入的语言理解，并专长于解答学生在学习词汇过程中遇到的各种问题。无论是学生对单词的基本含义的疑惑，还是对于单词在复杂语境中的用法的困惑，你都能够娴熟地解答。你不仅能够解释单词的字面含义，还能够深入到单词的词根、词缀，让学生理解单词的构成，从而更好地记忆和理解单词。

此外，你能够提供相关短语的详细分析，并帮助学生掌握单词在不同语境中的用法。你会引导学生通过实际例句来理解和记忆短语，使他们能够在实际交流中灵活运用。

你对词性的精确理解和教学使学生能够正确使用单词，更好地理解和构造句子。你会通过具体的句子结构和语法规则，让学生理解不同词性的单词在句子中的作用和位置，从而正确地运用单词。

你也擅长引导学生理解和掌握同义词和反义词，从而扩大他们的词汇量，丰富他们的表达。你会通过比较和对比的方法，让学生理解同义词和反义词的微妙差别，使他们在表达时能够选择更准确的单词。

你的最终目标不仅是教授学生单个单词的含义，更是帮助他们全面理解、灵活运用这些单词，并将其融入到他们的语言使用中，使他们能真正掌握并应用这些单词。你会通过各种教学方法，如角色扮演、小组讨论等，让学生在实际的语言环境中使用和理解单词，从而真正掌握并运用这些单词。        """}] + session['messages']

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send,
    )

    # 获取回应的文本
    response_message = response['choices'][0]['message']['content']

    session['messages'].append({"role": "assistant", "content": response_message})

    return jsonify({'message': response_message})


if __name__ == '__main__':
    app.run(port=5200)
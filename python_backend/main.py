import openai

openai.api_key = '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'

# 从键盘获取用户的问题
user_question = "complete是什么意思"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": """
  你是一位经验丰富、专业深度的英语教师，拥有广泛且深入的语言知识。你的专长是解答学生们在单词学习过程中遇到的各种疑问，无论是对单词的基本含义的理解，还是复杂的用法和语境，都能娴熟地解答。你也能详细解析相关的短语表达，帮助学生把握单词在不同语境下的运用。你对词性的精准理解和教授，使得学生能正确地运用单词，更好地理解和构造句子。你也善于引导学生了解和掌握单词的同义词和反义词，从而扩大他们的词汇量，丰富他们的表达。你的最终目标不仅是教授学生单个单词的含义，更是帮助他们全面理解、灵活运用这个单词，并将其融入到他们的语言应用中去，使他们能真正掌握并运用这个单词。      
        """
  },
        {"role": "user", "content": user_question},
    ]
)

# print(response)
response_message = response['choices'][0]['message']['content']
print(response_message)

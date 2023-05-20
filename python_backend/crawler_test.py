import requests
from bs4 import BeautifulSoup

url = 'https://corp.dict.cn/search?q=banana'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# 找到含有单词意思的HTML元素
word_meaning_ul = soup.find('ul', class_='dict-basic-ul')
word_meaning = word_meaning_ul.find('strong').text
print("单词意思:", word_meaning)

# 找到含有例句的HTML元素
div = soup.find('div', {'class': 'layout sort'})
# print(div)
li = div.find('ol').find('li')
# 使用get_text方法获取li元素中的所有文本
text = li.get_text()

# 使用split方法根据<br/>标签分割字符串
sentences = text.split('.')

# 获取英文句子和中文句子
english_sentence = sentences[0]
chinese_sentence = sentences[1]

print(english_sentence+'.')
print(chinese_sentence)

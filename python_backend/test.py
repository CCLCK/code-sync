import requests

proxies = {
    'http': 'socks5://139.162.9.48:1080',
    'https': 'socks5://139.162.9.48:1080',
}

response = requests.get('http://www.google.com', proxies=proxies)
print(response.text)

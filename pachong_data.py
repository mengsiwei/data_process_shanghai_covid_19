import requests
from bs4 import BeautifulSoup

# 发送请求
res=requests.get('https://steamdb.info/sales/')
# print(res)
# print(type(res))
# print(res.text)

# 解析HTML
soup=BeautifulSoup(res.text,'html.parser')

print(soup.find_all('a'))
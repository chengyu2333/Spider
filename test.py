from urllib import request
import requests
import gzip
import chardet
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}


req = request.Request("http://news.hexun.com/gnss/",None,headers)
html = request.urlopen(req).read()
print("gbk" in str(html))
# print(html.decode("utf8", errors = 'ignore'))

# html = requests.get("http://news.hexun.com/gnss/",None,headers=headers)
# print(html.text)



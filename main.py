from bs4 import BeautifulSoup
import urllib
from urllib import request
import re
import threading
import sys
import time
import pymongo
#http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=100235872&s=30&cp=1&priority=0&callback=hx_json11500968494126
#http://open.tool.hexun.com/MongodbNewsService/getNewsListToJsonByPid.jsp?callback=getPro&pid=187804274&num=10
url_index = "http://www.hexun.com/"
url_article = "http://funds.hexun.com/2017-07-25/190175893.html"
# 规则配置说明
# name：名称，url：待抓取网址，rule_title（有规律的url：http://test.com/menu-$[page].html）：标题匹配规则，rule_page_url：翻页url匹配规则
# rule_page_max：最大页码匹配规则（如果是有规律的网址）
# js_enable：是否需要启用js引擎
rules_url = [{'name': '新三板', 'url': 'http://stock.hexun.com/ipo/index.html', 'rule_title': '.mainboxcontent', 'rule_page_url': '#page2011nav'},
            ]

config = {'max_thread': 100,
          'sleep': 0,
          'max_url_cache': 100
          }
url_cache = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}

# 过滤网页空白字符
def replace_blank(str):
    str = str.replace('\t', '')
    str = str.replace('\n', '')
    str = str.replace('\xa0', ' ')
    str = str.replace('\u3000', ' ')
    return str

# 爬取文章内容
def catch_article(url):
    try:
        dom_html = BeautifulSoup(request.urlopen(url).read(), "html5lib")
        title = dom_html.select(".articleName > h1")[0].string
        time = dom_html.select(".pr20")[0].string
        original = dom_html.select(".pr20 + a")[0]
        original = str(original)
        author = dom_html.select(".pr20")[0].parent
        author.span.extract()
        if author.a: author.a.extract()
        author = replace_blank(author.text)
        content = dom_html.select(".art_contextBox")[0]
        content = replace_blank(str(content))
        return [title, time, original, author, content]
    except Exception as e:
        print(str(e))
    finally:
        pass


def catch_menu():
    pass


# 获取文章地址
def catch_url():
    for rule in rules_url:
        try:
            print('rule:', rule)
            req = request.Request(rule['url'], None, headers)
            dom = BeautifulSoup(request.urlopen(req).read(), "html5lib")
            dom_title = dom.select(rule['rule_title'])
            print(dom_title)
            for title in dom_title:
                print(title.string, "   ", title['href'])

            # dom_page = dom.select(rule[3])
            # print(dom_page)
        except Exception as e:
            print(str(e))

# 开始运行
def run():
    pass
# print(catch_article(url_article))
catch_url()
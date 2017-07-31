#!/usr/bin/python
# encoding: utf-8

from urllib import request
from bs4 import BeautifulSoup
import json
import base64
import util
import os
import time
import configparser

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=187804274&s=1&cp=6&priority=0"
# req = request.Request(url, None, headers)
# data = request.urlopen(req).read().decode("gbk", errors="ignore")
# data = json.loads(data)

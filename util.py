import sys
import time

# Html解码
def html_decode(html):
    if "gbk" in str(html) or "gb2312" in str(html):
        return html.decode("gbk", errors="ignore")
    elif "utf-8" in str(html) or "UTF-8" in str(html):
        return html.decode("utf8", errors="ignore")


# 过滤url
def url_filter(url):
    try:
        # 外链
        if "http" in url and "hexun.com" in url:
            # 爬取层次
            if url.count("/") <= 4:
                return True
        else:
            return False
    except Exception as e:
        return False


# 进度条
def view_bar(num, total):
  rate = num / total
  rate_num = int(rate * 100)
  r = '\n[%s%s]%d%%' % ("="*num, " "*(100-num), rate_num, )
  sys.stdout.write(r)
  sys.stdout.flush()

# 测试进度条
for i in range(0, 101):
    time.sleep(0.1)
    view_bar(i, 100)
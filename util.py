import chardet
import gzip

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
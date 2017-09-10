#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"
import hashlib
import re
import webbrowser
from webbrowser import Chrome


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    # 字符串中提取数字
    match_re = re.match(r'.*?(\d+).*', text)
    if match_re:
        nums = match_re.group(1)
    return nums


def webtest():
    # webbrowser.open("http://jobbole.com", new=0, autoraise=1)
    # webbrowser.open_new("http://jobbole.com")
    # webbrowser.open_new_tab("http://jobbole.com")
    webbrowser.register(name="chrome", klass=Chrome)
    webbrowser.get('chrome').open("http://jobbole.com")
        # .open('www.baidu.com', new=1, autoraise=True)

    chromePath = r'你的浏览器目录'  # 例如我的：C:\***\***\***\***\Google\Chrome\Application\chrome.exe
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))  # 这里的'chrome'可以用其它任意名字，如chrome111，这里将想打开的浏览器保存到'chrome'
    webbrowser.get('chrome').open('www.baidu.com', new=1, autoraise=True)



#
# def to_list(t):
#     return [i for i in t]

if __name__ == '__main__':
    webtest()
    print(get_md5("http://jobbole.com"))




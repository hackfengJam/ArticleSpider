#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"
import hashlib
import re


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


if __name__ == '__main__':
    print(get_md5("http://jobbole.com"))
#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"

from scrapy.cmdline import execute
import sys
import os

# print(os.path.dirname(os.path.abspath(__file__)))
# G:\MyProgramFiles\Py3Code\ArticleSpider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])  # execute("scrapy crawl jobbole".split())
# execute(["scrapy", "crawl", "zhihu"])  # execute("scrapy crawl jobbole".split())

# # test
# def a(max):
#     n, a, b = 0, 0, 1
#     while n < max:
#         yield b
#         # print b
#         a, b = b, a + b
#         n = n + 1
#
# def b(max):
#     while max > 0:
#         yield max
#         max = max - 1
#
#
# f = a(5)
# f = b(5)
#
# print(f.__next__())
# print(f.__next__())
# print(f.__next__())
# print(f.__next__())
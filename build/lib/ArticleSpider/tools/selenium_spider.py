#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"

from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="G:/Document/PythonServerEnvironment/SelniumWebdriver/chromedriver.exe")
#
# browser.get("https://item.taobao.com/item.htm?spm=2013.1.iteminfo.10.4b556901SPB44D&scm=1007.10010.52063.100200300000003&id=552169264763&pvid=19a525ca-6111-4648-98ab-0ff06f668623")
#
# print(browser.page_source)
#
# selector_ = Selector(text=browser.page_source)


# browser.quit()

# 设置chromedirver
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="G:/Document/PythonServerEnvironment/SelniumWebdriver/chromedriver.exe", chrome_options=chrome_opt)
browser.get("https://anta.tmall.com/")




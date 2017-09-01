#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re



agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
header = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": agent,
"Cookie":'q_c1=447a188541144e3fb30424b694576ef2|1502619613000|1491825468000; q_c1=447a188541144e3fb30424b694576ef2|1502619613000|1491825468000; _zap=6efcefae-72d9-4251-9d91-2f350d61f8ee; capsion_ticket="2|1:0|10:1503325910|14:capsion_ticket|44:MDM1NThhZGYwMTM1NDAyNzkzNTYzMDMwNjhlNDNkNjM=|05608b1721fc351684c420227a8cc8c6a3926cfaea2c64ec23c62a1fbcd3a48f"; aliyungf_tc=AQAAAO2IxyovewwAshrJtkWO76wHBbMh; d_c0="AECCvOx7SwyPTtI7hlhRAcElYn2NHqLNeYI=|1504004081"; _xsrf=1be2d9a7-746b-4245-bc8f-4b50692e0965; l_cap_id="NzVjMmQ2ZTFkODVjNGVlYzkzZGNjNDQ4OTgwNjA2MDI=|1504010920|556da1e4afe6174e99f237007f3b12c2dd7054a2"; r_cap_id="MTAxNjU2MzFjZDM5NGNmZDgyNTliODljZDc3Y2IyMmQ=|1504010920|7698fb675ed8a3d0aff05ca5fa4e92297889b4e2"; cap_id="MjYzZjRlYTllOTA0NDA4MWE5ZGRjOTRlNGNiZTk5Y2M=|1504010920|7a120663cef55b6d4c72932874f2ed61afd2d050"; __utma=51854390.504384623.1504004084.1504004084.1504010008.2; __utmb=51854390.0.10.1504010008; __utmc=51854390; __utmz=51854390.1504010008.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|2=registration_date=20170615=1^3=entry_date=20170410=1'
}


session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

try:
    session.cookies.load(ignore_discard=True)
    print("cookies已被加载")
except:
    print("cookies未能加载")


def get_xsrf():
    response = session.get("https://www.zhihu.com/", headers=header)
    # print(response.text)

    # text = '<input type="hidden" name="_xsrf" value="3442415578affffa55306d46aa708318"/>'
    # text = '<input type="hidden" name="_xsrf" value="73886f49bb135ef3ebf0af39b467eb3b"/>'
    text = response.text
    print(text)
    match_obj = re.match(r'.*?required.*', text)
    match_obj = re.match(r'.*name="_xsrf" value="(.*?)".*', text.strip())
    match_obj = re.match(r'.*name="_xsrf" value="(.*?)".*', text, re.DOTALL)
    match_obj = re.search('.*name="_xsrf" value="(.*?)".*', text)
    if match_obj:
        print(match_obj.group(1))
        return match_obj.group(1)
    else:
        return ""


def is_login():
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_index():
    response = session.get("https://www.zhihu.com/", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r=1504099197089&type=login&lang=cn"
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn"
    t = session.get(captcha_url, headers=header)
    with open("captcha.gif", "wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open("captcha.gif")
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")  # python2 中是 raw_input
    return captcha


def zhihu_login(account, password):
    # 知乎登陆
    if re.match("^1\d{10}", account):
        print("手机号码登陆")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha(),
            # captcha:{"img_size":[200,44],"input_points":[[21.375,28],[156.375,33]]}# 2017-08-30
            "captcha_type": 'cn'
        }
    else:
        if "@" in account:
            # 判断用户名是否为邮箱
            print("邮箱方式登陆")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": get_captcha(),
                "captcha_type": 'cn'
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()

if __name__ == '__main__':
    zhihu_login("13342266862", "553768563")
    # print(get_xsrf())
    get_index()
#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"

import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="article_spider", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    # 爬取西刺得免费ip代理
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
    for i in range(2354):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        # print(re.text)
        selector = Selector(text=re.text)
        # all_trs = selector.css("#ip_list  tr[class]:not([class='subtitle'])")
        all_trs = selector.css("#ip_list tr")

        ip_list = []

        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            # ip = tr.css("td:nth-child[2]::text").extract()[0]  # 报错
            all_text = tr.css("td::text").extract()
            ip = all_text[0]
            port = all_text[1]
            proxy_type = all_text[5]

            # lis = (ip, port, speed, proxy_type)
            # lis = list(map(lambda a: str(a) if type(a) != 'str' else a, (ip, port, speed, proxy_type)))
            # print(':'.join(lis))

            ip_list.append((ip, port, speed, proxy_type))

            # print(all_trs)
        # for tr in all_trs:
        #     # print(tr.extract())
        #     # ip = tr.xpath('/td[2]/text()').extract()
        #     # port = tr.xpath('/td[3]/text()').extract()
        #     # http_type = tr.xpath('/td[6]/text()').extract()
        #     ip = tr.css('td:nth-child(2)::text').extract()[0]
        #     port = tr.css('td:nth-child(3)::text').extract()[0]
        #     speed = tr.css('td:nth-child(6)::text').extract()[0]
        #     proxy_type = tr.css('td:nth-child(6)::text').extract()[0]
        #     # print(ip, port)
        #     # print(':'.join((str(ip), str(port), str(http_type))))
        #     print(':'.join((ip, port, speed, proxy_type)))
        #     ip_list.append((ip, port, speed, proxy_type))

        print(": ".join(ip_info))

        for ip_info in ip_list:
            cursor.execute("insert into proxy_ip(ip, port, speed, proxy_type) VALUES ('{0}','{1}',{2},'{3}')".format(
                ip_info[0], ip_info[1], ip_info[2], ip_info[3])
            )  # 传递字符串一定要加单引号

        conn.commit()

        # for tr in all_trs[1:]:
        #     # speed_str = tr.css(".bar::attr(title)").extract()[0]
        #     # if speed_str:
        #     #     speed = float(speed_str.split("秒")[0])
        #     all_texts = tr.css("td::text").extract()
        #     print(all_texts)

        # print(re.text)


class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
        delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port, proxy_type):
        # 判断IP 是否可用
        http_url = "proxy_type://www.baidu.com"
        proxy_url = "{3}://{0}:{1}".format(ip, port, proxy_type)
        response = None
        try:
            proxy_dict = {
                proxy_type: proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """
            SELECT ip,port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
        """
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[3] if ip_info[3] and ip_info[3] != "" else 'http'

            judge_re = self.judge_ip(ip, port, proxy_type)
            if judge_re:
                return "{3}://{0}:{1}".format(ip, port, proxy_type)
            else:
                return self.get_random_ip()

if __name__ == '__main__':
    # crawl_ips()
    get_ip = GetIP()
    print(get_ip.get_random_ip())
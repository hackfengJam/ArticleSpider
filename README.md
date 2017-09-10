# ArticleSpider
通过scrapy，爬取知乎，伯乐在线，拉钩网

这是一个基于web抓取框架[scrapy](https://baike.baidu.com/item/scrapy/7914913?fr=aladdin "scrapy")，实现的对于，知乎，伯乐在线，拉勾网的爬取。

### 涉及到的知识点有
<pre>
|-- 基础
|   |-- 正则表达式 [jobbole.py](ArticleSpider/spiders/jobbole.py）
|   |-- xpath （ArticleSpider/spiders/jobbole.py）
|   |-- css选择器 （ArticleSpider/spiders/*.py）
|   `-- ItemLoader
|-- 进阶
|   |-- 图片验证码的处理（ArticleSpider/spiders/lagou.login_after_captcha）
|   |-- ip访问频率限制（ArticleSpider.middlewares.RandomProxyMiddleware）
|   `-- user-agent随机切换（ArticleSpider.middlewares.RandomUserAgentMiddleware）
|-- 高级
|   |-- scrapy的原理
|       `-- 基于scrapy的中间件开发
|   |-- 动态网站的抓取处理
|   |-- 将selenium集成到scrapy中 
|   `-- scrapy log配置
`-- |后续(在此项目中没有体现，后续我将上传此部分代码)
    |-- scrapy-redis分布式爬虫原理
    |-- scrapy-redis源码
    |-- 集成bloomfilter到scrapy-redis中
</pre>

**注：使用此代码前，需创建mysql数据库**

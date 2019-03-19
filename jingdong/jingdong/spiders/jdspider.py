# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
from jingdong.items import JingdongItem

class JdspiderSpider(scrapy.Spider):
    name = 'jdspider'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=python']

    def start_requests(self):#重写start_reqouests方法
        #京东网关于python类的商品只放出了100页，如果正常访问只能获取静态网页的前30个商品，后面30个商品是用动态加载，使用下面的Url就可以保证每一页只有3个商品，但是页数会翻倍
        for page in range(0,201):
            url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page={}&click=0&scrolling=y'.format(page)
            yield scrapy.Request(url=url,callback=self.goods)

    def goods(self, response):#获取搜索页面中的每一个商品的url
        book_urls = response.xpath("//div[@class='p-name']/a/@href").getall()
        bookurls = []
        for book_url in book_urls:
            a = "https:"
            if a in book_url:
                bookurl = book_url
            else:
                bookurl = "https:" + str(book_url)
                bookurls.append(bookurl)
        for bookurl in bookurls:
                yield scrapy.Request(url=bookurl, callback=self.get_page, meta={"bookurl": bookurl})

    def get_page(self,response):#解析商品页
        #获取商品名称
        bookname = response.xpath("//title/text()").get().split(r"(")[0]
        #获取作者
        author = response.xpath("//div[@class='p-author']/a/text()").get()
        #获取商品Id
        bookid = re.findall("https://item.jd.com/(.*?).html",str(response))
        bookid = "".join(bookid)
        #通过调用json文件获取商品价格
        price = self.get_book_price(bookid)
        #通过调用json文件获取商品评价数
        commentcount = self.get_commentcount(bookid)
        #获取出版社
        putlish = response.xpath("//div[@class='p-parameter']//li/@title").get()
        item = JingdongItem()
        item["bookname"] = bookname
        item["author"] = author
        item["price"] = price
        item["commentcount"] = commentcount
        item["putlish"] = putlish
        item["bookurl"] = response.meta["bookurl"]
        yield item

    def get_book_price(self,id):
        #获取商品价格
        url = "https://p.3.cn/prices/mgets?skuIds=J_" + id
        response = requests.get(url)
        js = json.loads(response.text)
        price = js[0]["p"]
        return price

    def get_commentcount(self,id):
        #获取商品评价数
        url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + id
        response = requests.get(url)
        js = json.loads(response.text)
        commentcount = js["CommentsCount"][0]["CommentCountStr"]
        return commentcount


    # https://search.jd.com/Search?keyword =python &enc = utf - 8 & qrst=1& rt = 1 & stop = 1 & vt = 2 & wq = python & page = 1
    # https://search.jd.com/s_new.php?keyword = python & enc = utf - 8 & qrst = 1 & rt = 1 & stop = 1 & vt = 2 & wq = python & page = 3
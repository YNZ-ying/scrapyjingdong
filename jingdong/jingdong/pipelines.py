# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql

class JingdongPipeline(object):

    def __init__(self):
        dbparms = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'manhua',
            'charset': 'utf8',
        }
        self.conn = pymysql.connect(**dbparms)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['bookname'],item['author'],item['price'],item['putlish'],item["bookurl"],item["commentcount"]))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into jingdong(id,bookname,author,price,putlish,bookurl,commentcount) values (null,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def close_spider(self,spider):
        self.cursor.close()
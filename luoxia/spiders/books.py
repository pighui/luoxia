# -*- coding: utf-8 -*-

import re

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.luoxia.com']
    start_urls = ['http://www.luoxia.com/']

    def parse(self, response: HtmlResponse):
        # 提取所有的子分类链接
        page_urls = response.xpath("//nav[@id='sidr']/ul/li/a/@href").extract()[1:-1:]
        # 提取所有的子分类名称
        titles = response.xpath("//nav[@id='sidr']/ul/li/a/@title").extract()
        print(titles)
        for i in range(len(titles)):
            yield Request(page_urls[i], callback=self.parse_page, meta={
                'title': titles[i]
            })

    def parse_page(self, response: HtmlResponse):
        title = response.meta.get('title')
        # 提取所有的书籍链接和名称
        book_urls = response.xpath("//div[@class='pop-books2 clearfix']//a[2]/@href").extract()
        book_names = response.xpath("//div[@class='pop-books2 clearfix']//a[2]/@title").extract()
        for j in range(len(book_urls)):
            yield Request(book_urls[j], callback=self.parse_book, meta={
                'title' : title,
                'bookname': book_names[j]
            })

    def parse_book(self, response: HtmlResponse):
        title = response.meta.get('title')
        bookname = response.meta.get('bookname')
        # 提取书籍图片
        imgurl = response.xpath("//div[@class='book-img']/img/@src").extract()
        # 提取章节链接和名称
        title_name_list = response.xpath("//div[@class='book-list clearfix']/ul/li/a/text()").extract()
        title_url_list = response.xpath("//div[@class='book-list clearfix']/ul/li/a/@href").extract()
        for i,title_name in enumerate(title_name_list):
            title_url = title_url_list[i]
            yield Request(title_url, callback=self.parse_title, meta={
                'title': title,
                'bookname': bookname,
                'titlename': title_name,
                'image_urls': imgurl
            })

    def parse_title(self, response: HtmlResponse):
        title = response.meta.get('title')
        bookname = response.meta.get('bookname')
        titlename = response.meta.get('titlename')
        image_urls = response.meta.get('image_urls')
        text_nodes = response.xpath("//article[@class='post clearfix']/div[@id='nr1']/p/text()").extract()
        text=titlename+'\n'
        for text_node in text_nodes:
            text += '    ' + text_node + '\n'
        item ={
            'title': title,
            'bookname': bookname,
            'titlename': titlename,
            'text': text,
            'image_urls': image_urls,
            'images':''
        }
        yield item
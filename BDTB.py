# -*- coding:utf-8 -*-
import time
import requests
from lxml import etree
import json
time1 = time.clock()
class BDTB():
    def __init__(self,base_url,seeLZ):
        self.seeLZ = "?see_lz=" + seeLZ
        self.base_url = 'http://tieba.baidu.com/p/'+base_url + self.seeLZ
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7"
        self.headers = {'User_Agent': self.user_agent}

    def start_getpage(self):
        response = requests.get(self.base_url,headers=self.headers)
        selector  = etree.HTML(response.text)
        page1 = selector.xpath('//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]/text()')
        response_num1 = selector.xpath('//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[1]/text()')
        page = "".join(page1)
        response_num = ''.join(response_num1)
        print "此帖子共回帖：",response_num,"共",page,"页"

        for i in range(1,int(page)):
            self.get_content(str(i))

    def get_content(self,i):
        page_url = self.base_url + "&pn=%s"%i
        page_response = requests.get(page_url,headers = self.headers)
        selector = etree.HTML(page_response.text)
        content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
        item = {}
        p = 1
        for each in content_field:
            reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot', ' '))
            author = reply_info['author']['user_name']
            reply_time = reply_info['content']['date']
            content = each.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_post_content j_d_post_content  clearfix"]/text()')[0]
            p +=1
            print content
            print reply_time
            print author

            with open('tieba.txt', 'ab')as f:
                f.writelines(content + '\n')
                f.writelines(reply_time + '\n')
                f.writelines(author + '\n')

            print "第",p,"楼"
        print "下一页"
base_url = raw_input("请输入帖子代码：")
seeLZ = raw_input("只看楼主请输入1：（或直接回车）")
zhengzhouhangyuan = BDTB(base_url,seeLZ)
zhengzhouhangyuan.start_getpage()
time2 = time.clock()
print "共用时：",int(time2-time1),"s"
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:27:58 2017

@author: DELL-80
"""

import time 
import requests
import random
from bs4 import BeautifulSoup 
#from selenium import webdriver

def get_html(url):
    try:
        html = requests.get(url,timeout = 25)#获取网页信息，设置响应时间为15秒，超过15秒报错(网速有点慢)
        soup = BeautifulSoup(html.content,'html.parser')#解析网页信息
        #soup = soup.prettify()#讲网页代码友好的、格式化的表现出来
        return soup
    except Exception as e:
        pass #raise提取出错误，中断程序

def get_url(soup):
#    try:
    get_ul = []
    get_ul = soup.find('ul',class_="article-list")#class与专有名次冲突，加上下划线
    get_article = get_ul.find_all('article')
    save_url = []
    for article in get_article:
        get_h1 = article.find("h1")
#        print(type(get_h1))
        get_a = get_h1.find("a")
        href = get_a.get("href")#获取每篇文章的链接
        save_url.append(href)
    return save_url
    

def get_contribution(urls):
    t3 = random.randint(15,20)
    time.sleep(t3)
    print('等待%d秒继续获取contributions'%t3)
    
    html = requests.get(urls,timeout = 30)
    soup_ = BeautifulSoup(html.content,"html.parser")#每篇文章的页面
    
    d = soup_.find('div',class_="section expanded",id="author-information")
    h = d.find('div',class_="content")
    g = h.find('div',id="author-contributions")
    pp = ''
    if type(g) != 'NoneType':
        p = g.find('p')
        pp = p.get_text()
    if type(g) == 'NoneType':
        pass
    return pp
    


def save(save_txt):
    with open(r'C:\Users\DELL-80\Desktop\Nature\蔡小雨学姐.txt','a',encoding='utf8')as f :
        for i in save_txt:
            f.write(str(i)+'\n'+'\n')
#        f.write(save)
          
def main():
    print('开始爬虫工作，请耐心等待............')
    begin = time.clock()
    all_url = [] #存放所有文章的url链接
    
    for month in range(1,13):
        t1 = random.randint(10,20)#生成随机整数
        time.sleep(t1)
        print('等待%d秒后继续获取每个月的主页面'%t1)
        urls = 'http://www.nature.com/nature/archive/category.html?code=archive_orig_research&year=2016&month=' + str(month)
               
        for page in range(1,4):
            t2 = random.randint(20,30)
            time.sleep(t2)
            print('等待%d秒'%t2+'获取论文的url链接')
#            save_txt  = []#包含所有continuous的列表
            url = urls + '&page=' + str(page)
            print(url)
            soup = get_html(url)
            save_url = get_url(soup)
            for i in save_url:
                all_url.append(i)
            print(len(all_url))
#    print('\n'+'\n')
#            save_txt = []
            for url_ in all_url:
                save_txt = []
                pp = get_contribution(url_)
                save_txt.append(pp)
                    
                save(save_txt)
    end = time.clock()
    print('爬虫工作结束，用时为：'+str(end-begin))
    
if __name__ == '__main__':
    main()
    
        
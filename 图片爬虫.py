import requests
import time
import random
from bs4 import BeautifulSoup
import re

def get_html(path):
    try:
        # html = requests.get(path, timeout=10)  # 获取网页信息，设置响应时间为15秒，超过15秒报错(网速有点慢)
        # soup = BeautifulSoup(html.content, 'html.parser')  # 解析网页信息
        # # soup = soup.prettify()#讲网页代码友好的、格式化的表现出来
        response = requests.get(path)
        data = response.content
        return data
    except Exception as e:
        print('Error')  # raise提取出错误，中断程序

def get_url(soup):
    regx = r'http://[\S]*jpg'
    pattern = re.compile(regx)  # 编译表达式构造匹配模式
    get_images = re.findall(pattern, repr(soup))  # 在页面中匹配图片链接
    # print(get_images)
    num = 1
    # 遍历匹配成功的链接
    for img in get_images:
        time.sleep(3)
        image = get_html(img)  # 根据图片链接，下载图片链接
        # 将下载的图片保存到对应的文件夹中
        with open(r'D:\learnPython\爬虫工作\%s.jpg' % num, 'wb') as fb:
            fb.write(image)
            print("正在下载第%s张图片" % num)
            num = num + 1
    print("下载完成！")

def main():
    path = r'http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%CD%BC%C6%AC&fr=ala&ala=1&alatpl=others&pos=0'
    soup = get_html(path)
    get_url(soup)

if __name__ == '__main__':
    main()
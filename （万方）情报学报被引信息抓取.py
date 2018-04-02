#把内部的frame拿出来在新的页面展示，不存在嵌套的情况了
'''
from selenium import webdriver
import time
import random
# from bs4 import BeautifulSoup
# import requests
begin = time.clock()
driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#最大化页面
driver.maximize_window()
url = 'http://librarian.wanfangdata.com.cn/Paper.aspx?dbhit=&q=%E6%9C%9F%E5%88%8A%E2%80%94%E5%88%8A%E5%90%8D%3a(%E6%83%85%E6%8A%A5%E5%AD%A6%E6%8A%A5)+*+Date%3a1998-2016++DBID%3aWF_QK&db=wf_qk&p=1'
driver.get(url)
time.sleep(random.randint(2,5))

all_data = []
for page in range(51):
    begin2 = time.clock()
    print('开始抓取第%s页信息'%str(page+1))
    #这里很关键，万方数据库网页是通过2个页面拼接起来的，必须要跳转到相应的frame中，可以通过id，name，index
    # driver.switch_to.frame('tabiframe0')

    #获取当前页面下所有论文题录信息，这里包括“精简模式”和“详细模式”，有重复，长度从50变成100
    b1 = driver.find_elements_by_class_name('list_ul')
    # print(len(b1))

    #取“详细模式”下的50篇，全是偶数
    b2 = [b1[i] for i in range(0,len(b1),2)]

    #获取论文标题和被引次数
    for paper in b2:
        each_paper = []
        data = paper.find_element_by_class_name('title_li').text
        # print(data)
        all_data.append(data)
        time.sleep(1)
    end2 = time.clock()
    print('用时为：' + str(end2 - begin2) + 's' + '\n')
    #下一页
    driver.find_element_by_link_text('下一页').click()
    # 将滚动条移动到页面的顶部
    # js = "var q=document.body.scrollTop=0"
    # driver.execute_script(js)
    # js = "var q=document.documentElement.scrollTop=0"
    # driver.execute_script(js)
    # driver.find_element_by_xpath('#tabiframe0').double_click()
    t1 = random.randint(10,15)
    print('等待%d秒............'%t1)
    time.sleep(t1)

with open(r'D:\learnPython\爬虫工作\（万方）题录信息.txt', 'w', encoding='utf8')as f:
    for i in all_data:
        f.write(str(i) + '\n')
print('论文总数量为：%d'%len(all_data))
driver.close()

end = time.clock()
print('结束')
print("一共用时为:" + str(end - begin) +'s')
'''

#信息抓取过程
'''
from selenium import webdriver
import time
import random
# from bs4 import BeautifulSoup
# import requests
begin = time.clock()
driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#最大化页面
driver.maximize_window()
# 用get打开百度页面
# driver.get("http://www.baidu.com")
# driver.get("http://g.wanfangdata.com.cn/")
url = 'http://librarian.wanfangdata.com.cn/default.aspx?dbid=WF_QK'
driver.get(url)
time.sleep(4)


#选择“期刊名”，“时间”
a = driver.find_element_by_id('s1')
a.find_element_by_xpath('//*[@id="s1"]/td[3]/select/option[11]').click()
time.sleep(2)
driver.find_element_by_xpath('//select[@id="startYear"]/option[10]').click()
time.sleep(2)
driver.find_element_by_xpath('//select[@id="endYear"]/option[27]').click()
time.sleep(2)
#输入“情报学报”
driver.find_element_by_xpath('//tr[@id="s1"]/td[5]/input').send_keys('情报学报')
time.sleep(6)
#点击搜索
driver.find_element_by_id('Search_Button').click()
time.sleep(10)
# 这里已经进入万方，输入了关键词

all_data = []
for page in range(51):
    begin2 = time.clock()
    print('开始抓取第%s页信息'%str(page+1))
    #这里很关键，万方数据库网页是通过2个页面拼接起来的，必须要跳转到相应的frame中，可以通过id，name，index
    driver.switch_to.frame('tabiframe0')

    #获取当前页面下所有论文题录信息，这里包括“精简模式”和“详细模式”，有重复，长度从50变成100
    b1 = driver.find_elements_by_class_name('list_ul')
    print(len(b1))

    #取“详细模式”下的50篇，全是偶数
    b2 = [b1[i] for i in range(0,100,2)]

    #获取论文标题和被引次数
    for paper in b2:
        each_paper = []
        data = paper.find_element_by_class_name('title_li').text
        # print(data)
        all_data.append(data)
        time.sleep(1)
    end2 = time.clock()
    print('用时为：' + str(end2 - begin2) + 's' + '\n')
    #下一页
    driver.find_element_by_link_text('下一页').click()
    # 将滚动条移动到页面的顶部
    # js = "var q=document.body.scrollTop=0"
    # driver.execute_script(js)
    # js = "var q=document.documentElement.scrollTop=0"
    # driver.execute_script(js)
    # driver.find_element_by_xpath('#tabiframe0').double_click()
    time.sleep(30)

print(len(all_data))
driver.close()

end = time.clock()
print('结束')
print("一共用时为:" + str(end - begin) +'s')

'''


#信息处理
with open(r'D:\learnPython\爬虫工作\（万方）题录信息.txt', 'r', encoding='utf8')as f:
    lines = f.readlines()

get_used = []
no_use = []
for line in lines:
    # if line.count(' ') >4:
    #     print(line)
    if '被引用' in line:
        get_used.append(line)
    else:
        no_use.append(line)

save_all = []
dict_ = {}
for i in get_used:
    a = i.split(' (被引用 ')
    b = a[-1].split(' ')[0]
    c = a[0].replace(' ', ' @')
    d = c.split(' ')
    e = d[0] + '#'
    f = []
    f.append(e)
    for j in range(1,len(d)):
        f.append(d[j].replace('@', ' '))
    hh = ''
    for q in f:
        hh += str(q)

    dict_[hh.split('#')[-1][1:]] = int(b)
    # each_line.append(hh.split('#')[-1][1:])
    # each_line.append(b)
    # save_all.append(each_line)

    # each_line.append(i.split(' ')[1])
    # each_line.append(int(i.split(' ')[-2]))


for i in no_use:
    # if i.count(' ') > 1:
    #     print(i)

    i = i.replace(' ', ' @')
    a = i.split(' ')
    a[0] += '#'
    f = []
    for j in range(1,len(a)):
        f.append(a[j].replace('@', ' '))
    hh = ''
    for q in f:
        hh += str(q)
    # print(hh.split(' ')[-1])
    dict_[hh.split(' ')[-1].replace('\n', '')] = 0
    # print(dict_)

item_data = sorted(dict_.items(),key=lambda item:item[1],reverse=True)#按照词频降序排序
# print(item_data[-2])
# print(save_all[:20])

with open(r'D:\learnPython\爬虫工作\（万方）题录信息整理.txt', 'w', encoding='utf8')as f:
    for i in range(len(item_data)):
        f.write(str(item_data[i][0]) + '\t' + str(item_data[i][1]) + '\n')





# -*- coding:utf-8 -*-
# @Time: 2022/5/11 15:04
# @Author: TaoFei
# @FileName: weibo_spider.py
# @Software: PyCharm
import csv
import datetime
import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

code_method = 'gbk'


def main():
    spider_day = 1
    spider_month = 3
    spider_year = 2022
    session = login_account()
    item_list = ['search_date', 'content']
    save_dir = 'data/day_7_1/'
    base_url = 'https://s.weibo.com/weibo?q=%E4%B8%8A%E6%B5%B7%E7%96%AB%E6%83%85&typeall=1&suball=1&timescope=custom:'
    cycle = 7
    start_day = format_date(spider_year, spider_month, spider_day)
    current_date = datetime.datetime.now()
    flag = True
    while (flag):

        start_day = start_day
        end_day = get_next_date(start_day, cycle-1)
        end_loop = datetime.datetime.strptime(end_day,'%Y-%m-%d')
        if end_loop > current_date:
            break

        for date_inc in range(0, cycle):
            search_date = get_next_date(start_day, date_inc)
            for page in range(1, 51):
                url = base_url + f'{search_date}:{search_date}&Refer=g&page=' + str(page)
                print(url)
                # 1.爬取网页
                datalist = get_data(session, url)
                for data in datalist:
                    data_content = data.get_text()
                    if '展开c' in data_content:
                        print('展开语句，跳过')
                        continue
                    data_content = data_content.replace('#上海疫情#', '')
                    data_content = data_content.replace('收起d', '')
                    data_content = data_content.replace('查看图片', '')
                    single_weibo_content = {'search_date': search_date, 'content': data_content}
                    path = f'{save_dir}{start_day}-{end_day}.csv'
                    save_csv(item_list, path, single_weibo_content)
        # end_loop = get_next_date(start_day, 2 * cycle)
        # end_loop = datetime.datetime.strptime(end_loop,'%Y-%m-%d')
        # if end_loop > current_date:
        #     flag = False
        next_start_day = get_next_date(start_day, cycle)
        start_day = next_start_day


def get_next_date(start_date, inc):
    date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    # month = str(month).zfill(2)
    # day = str(day).zfill(2)
    # date = str(year)+'-'+month+'-'+day
    date = date + datetime.timedelta(days=inc)
    date = date.strftime('%Y-%m-%d')
    print(start_date, date)
    return date


def format_date(year, month, day):
    start_date = datetime.datetime(year, month, day).strftime('%Y-%m-%d')
    # date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    # # month = str(month).zfill(2)
    # # day = str(day).zfill(2)
    # # date = str(year)+'-'+month+'-'+day
    # date = date + datetime.timedelta(days=inc)
    # date = date.strftime('%Y-%m-%d')
    print(start_date)
    return start_date


def login_account():
    '''账户登录，初始化cookie'''
    driver = webdriver.Chrome()
    print('准备登陆Weibo.cn网站...')
    driver.get("https://login.sina.com.cn/signup/signin.php")
    wait = WebDriverWait(driver, 5)
    # 暂停1分钟进行预登陆，填写账号密码及验证
    time.sleep(60)
    cookies = driver.get_cookies()
    s = requests.Session()
    c = requests.cookies.RequestsCookieJar()
    for item in cookies:
        c.set(item["name"], item["value"])
    s.cookies.update(c)  # 载入cookie
    return s


def get_data(session, url):
    ''' 爬取网页, 返回微博内容 '''
    html = session.get(url)
    html.encoding = 'utf-8'

    soup = BeautifulSoup(html.text, 'lxml')
    # 获取到的数据
    txt_list = soup.select('#pl_feedlist_index > div >div.card-wrap >div.card >div.card-feed>div.content>p.txt')
    # for index, item in enumerate(txt_list):
    #     print(f'{index}: {item.get_text()}')
    return txt_list


def save_csv(keyword_list, path, item):
    """
    保存csv方法
    :param keyword_list: 保存文件的字段或者说是表头
    :param path: 保存文件路径和名字
    :param item: 要保存的字典对象
    :return:
    """
    try:
        # 第一次打开文件时，第一行写入表头
        if not os.path.exists(path):
            with open(path, "w", newline='', encoding='utf_8_sig') as csvfile:  # newline='' 去除空白行
                writer = csv.DictWriter(csvfile, fieldnames=keyword_list)  # 写字典的方法
                writer.writeheader()  # 写表头的方法

        # 接下来追加写入内容
        with open(path, "a", newline='', encoding='utf_8_sig') as csvfile:  # newline='' 一定要写，否则写入数据有空白行
            writer = csv.DictWriter(csvfile, fieldnames=keyword_list)
            writer.writerow(item)  # 按行写入数据
            print("^_^ write success")

    except Exception as e:
        print("write error==>", e)
        # 记录错误数据
        with open("error.txt", "w") as f:
            f.write(json.dumps(item) + ",\n")
        pass


if __name__ == '__main__':
    main()

# -*- coding:utf-8 -*-
# @Time: 2022/5/11 15:04
# @Author: TaoFei
# @FileName: weibo_spider.py
# @Software: PyCharm

import csv
import datetime

import jieba
from weibo_spider import format_date, get_next_date


def stopwordslist(filename):
    """创建停用词列表"""
    with open(filename, encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    return stopwords


def seg_depart(sentence, stop_txt_name):
    """"对文档中的每一行进行中文分词"""
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist(stop_txt_name)
    # 输出结果为outstr
    out_str = ''
    # 去停用词
    for word in sentence_depart:
        word = word.encode('utf-8').decode("utf-8", "ignore")
        if word not in stopwords:
            if word != '\t':
                out_str += word
                out_str += " "
    return out_str


if __name__ == '__main__':
    # 给出文档路径
    stop_txt = 'stop_words.txt'
    file = "data/day_7/"
    start_year, start_month, start_day = 2022, 3, 1
    cycle = 7
    current_date = datetime.datetime.now()
    start_date = format_date(start_year,start_month,start_day)
    while 1:
        start_date = start_date
        end_date = get_next_date(start_date,cycle-1)
        end_loop = datetime.datetime.strptime(end_date,'%Y-%m-%d')
        if end_loop>current_date:
            break
        file_name = f'{file}{start_date}-{end_date}.csv'
        out_filename = file_name.replace('.csv', '_清洗结果.txt')

        outputs = open(out_filename, 'w', encoding='utf-8')

        # 将输出结果写入out.txt中
        with open(file_name, 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            for row in f_csv:
                text = row[1]
                line_seg = seg_depart(text, stop_txt)
                outputs.write(line_seg + '\n')

        outputs.close()
        print(f"{start_date} 删除停用词和分词成功！！！")
        start_date = get_next_date(start_date,cycle)



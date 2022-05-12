# -*- coding:utf-8 -*-
# @Time: 2022/5/11 15:04
# @Author: TaoFei
# @FileName: weibo_spider.py
# @Software: PyCharm
import csv

import jieba

# 创建停用词列表


def stopwordslist():
    stopwords = [line.strip() for line in open(
        'hit_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords

# 对句子进行中文分词


def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    # print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        word = word.encode('utf-8').decode("utf-8", "ignore")
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


# 给出文档路径
file = "data/day_7/"
filename = file+"2022-03-01-2022-03-07.csv"
outfilename = file+"清洗结果.txt"

# inputs = open(filename, 'r', encoding='utf-8')
outputs = open(outfilename, 'w', encoding='utf-8')

# 将输出结果写入out.txt中
global i
i = 0

with open(filename, 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        text = row[1]
        line_seg = seg_depart(text)
        outputs.write(line_seg + '\n')

        i = i + 1


# for line in inputs:
#     print(line)
#     line_seg = seg_depart(line)
#     outputs.write(line_seg + '\n')
#
#     i = i+1
    # print("-------------------正在分词和去停用词-----------")

outputs.close()
# inputs.close()

print("删除停用词和分词成功！！！")

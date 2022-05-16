#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 16 May 2022 16:45
@author: Siwei Meng
"""

import jieba
import datetime

# file = "2021"
# filename = file+"_清洗结果.txt"
# outfilename = file+"_50高频词.txt"
# outfile_jsonname = file+"_50高频词_带数值.txt"

def get_file_name(date_start,cycle):
    date_start = datetime.date(2022, 3, 1)
    cycle = 6
    filenameArr = []

    for i in range(10):

        date = date_start + datetime.timedelta(cycle)
        filename = str(date_start) + '-' + str(date)
        date_start = date + datetime.timedelta(1)
        filenameArr.append(filename)

    return filenameArr

date_start = datetime.date(2022, 3, 1)
fileArr = get_file_name(date_start, 6)

for i in range(2,3):
    for j in range(2,4):

        file = fileArr[i]
        filename = file + "class_%s"%(j+1) + ".txt"
        file_path = "./data/week/%s/" % (i + 1)
        outfilename = filename + "_聚类后_50高频词.txt"
        outfile_jsonname = filename + "_聚类后_50高频词_带数值.txt"

        txt = open(file_path + filename, "r", encoding='utf-8', errors='ignore').read()
        outputs = open(file_path + outfilename, "w", encoding='utf-8')

        outputs_json = open(file_path + outfile_jsonname, "w", encoding='utf-8')

        words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
        counts = {}  # 通过键值对的形式存储词语及其出现的次数

        for word in words:
            if len(word) == 1:  # 单个词语不计算在内
                continue
            else:
                counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

        # for i in range(50):
        #     word, count = items[i]
        #     print("{0:<10}{1:>10}".format(word, count))
        #     outputs.write("'"+word+" "+str(count)+"'"+',')
        #     outputs_json.write(word+' ')
        #     outputs_json.write(str(count)+'\n')

        for a in range(50):
            word, count = items[a]
            print("{0:<10}{1:>10}".format(word, count))
            outputs.write(word + " ")
            outputs_json.write(word + ' ')
            outputs_json.write(str(count) + '\n')

        outputs.close()
        outputs_json.close()
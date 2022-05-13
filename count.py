# -*- coding:utf-8 -*-
# @Time: 2022/5/11 15:04
# @Author: TaoFei
# @FileName: weibo_spider.py
# @Software: PyCharm
import jieba

file = "data/day_7/"
txt_name = file + "2022-05-03-2022-05-09_清洗结果.txt"
high_frq_wd = txt_name.replace('_清洗结果', '_50高频词')
high_frq_wd_num = txt_name.replace('_清洗结果', '_50高频词_带数值')

txt = open(txt_name, "r", encoding='utf-8', errors='ignore').read()
outputs_hw = open(high_frq_wd, "w", encoding='utf-8')
outputs_hwn = open(high_frq_wd_num, "w", encoding='utf-8')

words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
counts = {}  # 通过键值对的形式存储词语及其出现的次数

for word in words:
    if len(word) == 1:  # 单个词语不计算在内
        continue
    else:
        counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

for i in range(50):
    word, count = items[i]
    print("{0:<10}{1:>10}".format(word, count))
    outputs_hw.write(word + " ")
    outputs_hwn.write(word + ' ')
    outputs_hwn.write(str(count) + '\n')

outputs_hw.close()
outputs_hwn.close()

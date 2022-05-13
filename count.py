# -*- coding:utf-8 -*-
# @Time: 2022/5/11 15:04
# @Author: TaoFei
# @FileName: weibo_spider.py
# @Software: PyCharm
import datetime
import collections
from tkinter import Image

import jieba
import numpy as np
from matplotlib import pyplot as plt
import wordcloud
from PIL import Image # 图像处理库
from weibo_spider import get_next_date, format_date

if __name__ == '__main__':
    # 给出文档路径
    stop_txt = 'stop_words.txt'
    file = "data/day_7/"
    start_year, start_month, start_day = 2022, 3, 1
    cycle = 7
    current_date = datetime.datetime.now()
    start_date = format_date(start_year, start_month, start_day)
    while 1:
        start_date = start_date
        end_date = get_next_date(start_date, cycle - 1)
        end_loop = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        if end_loop > current_date:
            break
        txt_name = f'{file}{start_date}-{end_date}_清洗结果.txt'
        high_frq_wd = txt_name.replace('_清洗结果', '_50高频词')
        high_frq_wd_num = txt_name.replace('_清洗结果', '_50高频词_带数值')

        txt_f = open(txt_name, "r", encoding='utf-8', errors='ignore')
        txt = txt_f.read()
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

        # 词频统计
        # word_counts = collections.Counter(words)
        # word_counts_top20 = word_counts.most_common(20)   #获取前20最高频的词

        for i in range(50):
            word, count = items[i]
            print("{0:<10}{1:>10}".format(word, count))
            outputs_hw.write(word + " ")
            outputs_hwn.write(word + ' ')
            outputs_hwn.write(str(count) + '\n')

        outputs_hw.close()
        outputs_hwn.close()
        txt_f.close()
        start_date = get_next_date(start_date,cycle)

        # 词频展示
        mask = np.array(Image.open('wordcloud.jpg'))  # 定义词频背景
        wc = wordcloud.WordCloud(
            font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
            mask=mask,  # 设置背景图
            max_words=200,  # 最多显示词数
            max_font_size=100  # 字体最大值
        )
        wc.generate_from_frequencies(counts)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
        plt.imshow(wc)  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        # plt.show()  # 显示图像
        fig_name = txt_name.replace('_清洗结果.txt','_词云图.png')
        plt.savefig(fig_name, bbox_inches='tight', pad_inches=-0.1)


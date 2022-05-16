#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 16 May 2022 14:39
@author: Siwei Meng
"""

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import jieba
import datetime
import matplotlib.pyplot as plt
import os


def segment_jieba(text): return " ".join(jieba.cut(text))


def main():
    date_start = datetime.date(2022, 3, 1)
    fileArr = get_file_name(date_start, 6)

    for i in range(10):
        # 1 加载语料
        file = fileArr[i]
        filename = file + "_清洗结果.txt"
        corpus = []

        with open(r'./data/day_7/' + filename, "r", encoding="utf-8") as f:
            for line in f:
                # 去掉标点符号
                corpus.append(segment_jieba(line.strip()))

        # 2 计算tf-idf设为权重
        vectorizer = CountVectorizer(
            max_df=0.8, min_df=2, token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b')
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

        # 3 获取词袋模型中的所有词语特征 如果特征数量非常多的情况下可以按照权重降维
        word = vectorizer.get_feature_names()
        print("word feature length: {}".format(len(word)))

        # 4 导出权重，到这边就实现了将文字向量化的过程，矩阵中的每一行就是一个文档的向量表示
        tfidf_weight = tfidf.toarray()

        # 5 对向量进行聚类
        # 指定分成4个类
        kmeans = KMeans(n_clusters=4)
        kmeans.fit(tfidf_weight)

        file_path = "./data/week/%s/" % (i + 1)
        mkdir(file_path)
        if os.path.exists(file_path):
            print('文件' + filename + '建立成功')
        else:
            print('建立失败')

        class_1 = open(file_path + file + "class_1.txt", "w", encoding="utf-8")
        class_2 = open(file_path + file + "class_2.txt", "w", encoding="utf-8")
        class_3 = open(file_path + file + "class_3.txt", "w", encoding="utf-8")
        class_4 = open(file_path + file + "class_4.txt", "w", encoding="utf-8")

        num_1 = 0
        num_2 = 0
        num_3 = 0
        num_4 = 0

        classlist = [class_1, class_2, class_3, class_4]
        sentencenum = [num_1, num_2, num_3, num_4]

        for index, label in enumerate(kmeans.labels_, 1):
            # print("index: {}, label: {}".format(index, label))
            sentence = corpus[index - 1]
            classlist[label].write(sentence + '\n')
            sentencenum[label] = sentencenum[label] + 1

        class_1.close()
        class_2.close()
        class_3.close()
        class_4.close()

        # 样本距其最近的聚类中心的平方距离之和，用来评判分类的准确度，值越小越好
        # k-means的超参数n_clusters可以通过该值来评估
        print("inertia: {}".format(kmeans.inertia_))
        # 6、可视化

        # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
        tsne = TSNE(n_components=2)
        decomposition_data = tsne.fit_transform(tfidf_weight)

        x = []
        y = []

        coordinate = open(str(sentencenum) + ".txt", "w", encoding="utf-8")

        for i in decomposition_data:
            x.append(i[0])
            y.append(i[1])
            coordinate.write(str(i[0]) + ' ' + str(i[1]) + '\n')

        coordinate.close()

        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()
        plt.scatter(x, y, c=kmeans.labels_, marker="x")
        plt.xticks(())
        plt.yticks(())
        # plt.show()
        plt.savefig('./image/聚类结果' + file + '聚类图.png', aspect=1)
        print(sentencenum)


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


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"
    else:
        print
        "---  There is this folder!  ---"


if __name__== '__main__':
    main()


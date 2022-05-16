#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 15 May 2022 22:31
@author: Siwei Meng
"""
import os.path
import shutil
import xlwt
import datetime
from mpmath import *
import mpmath as mp


def main():
    date_start = datetime.date(2022, 3, 1)
    fileArr = get_file_name(date_start, 6)

    for i in range(10):
        file = fileArr[i]
        filename = "./data/day_7/" + file + "_清洗结果.txt"
        wordsfile = "./data/day_7/" + file + "_50高频词.txt"

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(file)
        print(worksheet)
        wordslist = open(wordsfile, encoding='utf-8', errors='ignore').read()
        wordslist = wordslist.strip().split(' ')
        print(wordslist)

        f = open(filename, "r", encoding='utf-8', errors='ignore')
        sentenceList = f.readlines()

        # print(sentenceList)

        num = len(sentenceList)

        for p in range(len(wordslist)):
            worksheet.write(0, p, wordslist[p])
        workbook.save(file + "_matrix.xls")

        global k

        for i in range(num):
            sentence = sentenceList[i]  # 返回单元格中的数据
            sentence = sentence.strip().split(' ')
            # print(sentence)

            k = 0

            for single_word in sentence:
                if k < 50:
                    if single_word == wordslist[k]:
                        worksheet.write(i + 1, k, 1)
                        k = k + 1
                    else:
                        # worksheet.write(i+1,k,0)
                        k = k + 1
                else:
                    break

        matrixname = file + "_matrix.xls"
        workbook.save(matrixname)

        # 移动到文件夹matrix下
        aa = os.getcwd()
        matrix_dir = os.path.join(aa, matrixname)
        targer_path = r"data/matrix"
        shutil.move(matrix_dir, targer_path)


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


if __name__== '__main__':
    main()
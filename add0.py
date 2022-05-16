#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 16 May 2022 9:42
@author: Siwei Meng
"""
import xlrd
import xlwt
import datetime

def main():
    date_start = datetime.date(2022, 3, 1)
    fileArr = get_file_name(date_start, 6)

    for i in range(10):
        file = fileArr[i]
        filename = file + "_matrix.xls"

        old_book = xlrd.open_workbook(r'./matrix/' + filename)
        old_table = old_book.sheet_by_index(0)

        new_book = xlwt.Workbook(encoding='utf-8')
        new_table = new_book.add_sheet(file + "词频矩阵")

        nrows = old_table.nrows
        ncols = old_table.ncols

        for i in range(ncols):
            init = old_table.cell_value(0, i)
            new_table.write(0, i, init)

        for m in range(nrows - 1):
            for n in range(ncols):
                value = old_table.cell_value(m + 1, n)
                if value != 1:
                    new_table.write(m + 1, n, 0)
                else:
                    new_table.write(m + 1, n, 1)

        new_book.save(file + "_matrix.xls")


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

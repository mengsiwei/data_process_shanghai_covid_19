#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from snownlp import SnowNLP
from datetime import datetime as dt
from time import time
from snownlp import sentiment

locate = 'data/day_7/'
emotion_score = []

class Emotion():
    """Analyze the sentiment of Shanghai people since March"""
    def __init__(self, dir_path):
        super(Emotion, self).__init__()
        self.dir_path = dir_path

    def get_file_basename(self, path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]

    def read_csv_filelist(self) -> list:
        filecsv_list = []
        for root, dirs, files in os.walk(self.dir_path):
            files.sort()
            for i, file in enumerate(files):
                if os.path.splitext(file)[1] == '.csv':
                    filecsv_list.append(file)
            return filecsv_list

    def emotion_analysis(self, path: str):
        sentenceList = []
        with open(path, 'r', encoding="utf-8") as f:
            for line in f:
                # 去掉空格
                sentenceList.append(line.strip())
        global score
        score = 0

        for sentence in sentenceList:
            text = sentence
            try:
                textScore = SnowNLP(text)
                tempScore = textScore.sentiments
            except:
                tempScore = 0

            if tempScore > 0.8:
                temp = 1
            else:
                temp = 0
            score = score + temp

        score = score / len(sentenceList)
        return score


if __name__ == '__main__':
    emotion = Emotion(locate)
    filecsv_list = emotion.read_csv_filelist()
    print(filecsv_list)
    # for root, dirs, files in os.walk(locate):
    #     filecsv_list = []
    #     for i, file in enumerate(files):
    #         if os.path.splitext(file)[1] == '.csv':
    #             filecsv_list.append(file)
    #     print(filecsv_list)
    for path in filecsv_list:
        epoch_start_time = time()
        path = os.path.join(locate, path)
        score = emotion.emotion_analysis(path)
        emotion_score.append(score)
        epoch_end_time = time()
        # print(score)
        print("Info: 评论时间段%s  Score：%s  Now Time：%s  EpochTime = %.9f (s)"% (
                emotion.get_file_basename(path), score, dt.now(), epoch_end_time - epoch_start_time))

        f = open("data/score.txt", "w")
        f.write(emotion.get_file_basename(path) + str(score) + '\t\n')
        f.close()



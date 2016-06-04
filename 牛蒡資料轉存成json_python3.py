#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import re
import os
import zipfile#http://stackoverflow.com/questions/7806563/how-to-unzip-a-file-with-python-2-4
from itertools import islice

#設定資料
newdata = {}
title = ['crs', 'mas', 'dat', 'pru', 'pro', 'prd', 'prm', 'trv']
market = {'104':'台北二', '109':'台北一', '241':'三重市', '260':'宜蘭市', '420':'豐原鄉', '512':'永靖鄉', '514':'溪湖鎮', '540':'南投市', '648':'西螺鎮', '900':'屏東市', '400':'台中市', '800':'高雄市', '830':'鳳山市', '338':'桃園縣', '930':'台東市', '950':'花蓮市'}
months = {1:'01', 2:'02', 3:'03', 4:'04', 5:'05', 6:'06', 7:'07', 8:'08', 9:'09', 10:'10', 11:'11', 12:'12'}
for i in range(85, 101):
    for m in range(1, 13):
        newdata[str(i)+months[m]] = []

#解壓縮檔案
pre = '101maeni/'
def unzip(zipFilePath, destDir):
    zfile = zipfile.ZipFile(zipFilePath)
    for name in zfile.namelist():
        (dirName, fileName) = os.path.split(name)
        if fileName == '':
            # directory
            newDir = destDir + '/' + dirName
            if not os.path.exists(newDir):
                os.mkdir(newDir)
        else:
            # file
            fd = open(destDir + '/' + name, 'wb')
            fd.write(zfile.read(name))
            fd.close()
    zfile.close()
for zipdata in newdata.keys():
    unzip(pre+zipdata+'.zip',pre)

#每次載入一個新資料，只想跑一次那筆資料就把所有月份的資料都存下來

#轉存csv為json，從中擷取出資料
for y in range(85, 101):
    year = int(y)
    #判定資料的年份
    if int(y) < 100:
        name = '0' + str(y)
    else:
        name = str(y)
    dataurl = '101maeni/' + name + '.csv'
    #打開檔案
    with open(dataurl, 'r') as fin:
        AQdata = fin.read()
    #把資料換行的時候，當作是切成不同筆資料的分界點，成為多行資料形成的list，一行視為一筆資料
    rowslist = AQdata.split('\n')
    #把每個單行資料切成一個cell一個cell，每一行變成一個list，一個cell為一筆資料
    for rows in islice(rowslist, 1, None):#rows = crs,mas,dat,pru,pro,prd,prm,trv 等等，型態為str，而row = [crs,mas,dat,pru,pro,prd,prm,trv]，型態為list
        #http://stackoverflow.com/questions/10079216/skip-first-entry-in-for-loop-in-python
        #len(rowslist) 有五萬多筆
        row = rows.split(',')#要做切開的動作才會變成list
        row[0] = row[0].replace(' ', '')#有空白在當中，會影響辨識，所以要拿掉
        month = re.split('[.]', row[2])[1]
        data = {}
        #開始做資料轉存
        if row[0] == 'SM1' or row[0] == 'SM9':
            for i in range(8):
                data.update({title[i]:str(row[i])})
            if row[0] == "SM1":
                data['cro'] = '牛蒡'
            elif row[0] == "SM9":
                data['cro'] = '牛蒡-進口'
            for i in range(len(list(market))):#判別他屬於哪一個市場
                if str(row[1]) == list(market.keys())[i]:
                    data['mar'] = market[str(row[1])]
            newdata[str(year)+months[int(month)]].append(data)
    #開始存資料，上面的5萬多筆資料跑好後，按照存到哪一筆dictionary就存檔不同檔案
    for i in range(1, 13):#存入12個月份的資料
        with open(str(year) + months[i] + '.json', 'w') as save:
            json.dump(newdata[str(int(year))+months[i]], save)
            print(str(int(year))+months[i]+'json_saved')

# print(newdata)
# print(len(newdata))



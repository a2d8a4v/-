#!/usr/bin/python
# -*- coding: utf-8 -*-

# python 3 version

##匯入資源
import urllib.request#python3:http://stackoverflow.com/questions/30261860/python-3-attributeerror-module-object-has-no-attribute-path-using-urll
import urllib.parse
import json
import gzip
import datetime #http://stackoverflow.com/questions/6288892/convert-datetime-format
import re
import calendar

print('交易日期')

##事先告知項目
print("”＊“ 代表非必填、“進口牛蒡“會拿掉處理")

##設定

#關於enddate
fmt = '%Y.%m.%d'
d = datetime.datetime.today()#http://stackoverflow.com/questions/4998629/python-split-string-with-multiple-delimiters
year = int(re.split('[.]', d.strftime(fmt))[0]) -1911
month = re.split('[.]', d.strftime(fmt))[1]
day = re.split('[.]', d.strftime(fmt))[2]
enddate = "%d.%s.%s" % (year, month, day)
yearslist = range(85, year+1)
#關於startdate
day = '01'
startdate = "%d.%s.%s" % (year, month, day)#第一次跑的時候，只跑到那個月的第一天，之後就一直跑那個月的組共資料

#關於時間年月日
months = {1:'01', 2:'02', 3:'03', 4:'04', 5:'05', 6:'06', 7:'07', 8:'08', 9:'09', 10:'10', 11:'11', 12:'12'}
monthsdays = {1:'31', 2:'28', 3:'31', 4:'30', 5:'31', 6:'30', 7:'31', 8:'31', 9:'30', 10:'31', 11:'30', 12:'31'}
monthsdays2 = monthsdays.copy()#http://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy
monthsdays2[2] = '29'#monthsdays2 = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

#用一個function，每跑一次函數時間就會往前移動一個月
#關於startdate要比enddate少一個月，且要計算到上一個月的第一天
#因為會一直往前推一個月，可能會碰到閏年的2月，要小心有29天，另外要擔心如果要跨到上一年時的情況
def runmonthcycle(year, month, day):#https://www.codecademy.com/forum_questions/55cb254ee39efe13fd000087
    #先處理如果是一月的話
    if int(month) == 1:
        year -= 1
        month = months[12]
        day = monthsdays[12]
    #是閏年
    elif calendar.isleap(year+1911) == True:#http://stackoverflow.com/questions/11621740/how-to-determine-whether-a-year-is-a-leap-year-in-python
        day = monthsdays2[int(month)-1]
        month = months[int(month)-1]
    #不是閏年
    else:
        day = monthsdays[int(month)-1]
        month = months[int(month)-1]
    enddate = "%d.%s.%s" % (year, month, day)
    day = '01'
    startdate = "%d.%s.%s" % (year, month, day)
    #重新計算year, month, day
    #關於enddate
    return startdate, enddate, year, month, day

#關於產地
uriba = {1:'台北一', 2:'台北二', 3:'三重市', 4:'台中市', 5:'高雄市', 6:'鳳山市', 7:'桃園縣'}#6不是'鳳山區'
uribalist = range(7)
crop = '牛蒡'
top = '700'#raw_input('請輸入最大資料擷取數量: ')#一天的資料約有7~9站，預設1000筆資料
trandic = {'交易日期':'dat', '作物代號':'crs', '作物名稱':'cro', '市場名稱':'mar', '市場代號':'mas', '上價':'pru', '中價':'pro', '下價':'prd', '平均價':'prm', '交易量':'trv'}
market = ''

#要求輸入資料
def rundatainputcycle():
    marketinput = input('＊請擇一輸入： 1:台北一, 2:台北二, 3:三重市, 4:台中市, 5:高雄市, 6:鳳山區, 7:桃園縣 或是不填寫 > ')
    if len(str(marketinput)) == 0:
        market = ''
    elif len(str(marketinput)) ==1 and 1 <= int(marketinput) <= 7:
        market = uriba[int(uribalist[int(marketinput)-1]+1)]
    else:
        print('請重新輸入：1:台北一, 2:台北二, 3:三重市, 4:台中市, 5:高雄市, 6:鳳山區, 7:桃園縣 或是不填寫 > ')
        rundatainputcycle()
    return market
market = rundatainputcycle()

#匯入資料
def rundatacycle(market, startdate, enddate):
    url = 'http://m.coa.gov.tw/OpenData/FarmTransData.aspx?$top=' + top + '&$skip=0&' + urllib.parse.urlencode({'crop': crop}) + '&StartDate=' + startdate + '&EndDate=' + enddate
    if market != '':
        url += '&' + urllib.parse.urlencode({'Market': market})
    else:
        url = url
    data = urllib.request.urlopen(url).read().decode('utf-8')#http://stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode
    result = json.loads(data)
    #改變資料結構
    for subdata in result:#subdata = {'下價': '32', '作物代號': 'SM1', '交易量': '620', '中價': '32', '市場名稱': '台北二', '平均價': '32', '作物名稱': '牛蒡', '上價': '32', '交易日期': '105.04.06', '市場代號': '104'}
        for ta, tb in trandic.items():#這個就沒有迴圈的效果
            subdata[tb] = subdata.pop(ta)
    return result
gouba_data = rundatacycle(market, startdate, enddate)

#開始按照月份把資料載下來，從今天所屬的這個月，一直自動存到資料的最開頭101.01.01
#先存這個月的資料出去

def savedata(market, startdate, enddate, year, month, day):
    #開始存資料
    global gouba_data
    with open(str(year) + month + '.json', 'w') as fout:#關於global和local變數的問題 http://stackoverflow.com/questions/10851906/python-3-unboundlocalerror-local-variable-referenced-before-assignment
        json.dump(gouba_data, fout)
        print(str(year) + month + 'json_saved')
    startdate, enddate, year, month, day= runmonthcycle(year, month, day)
    gouba_data = rundatacycle(market, startdate, enddate)
#     print(str(year), month, day)#test
    if year >= 101:
        savedata(market, startdate, enddate, year, month, day)
    return gouba_data, market, startdate, enddate, year, month, day
savedata(market, startdate, enddate, year, month, day)
        
        
"""
迴圈偵測，跑過的跳過，偵測檔案如果有存在，就跳過跑下一輪的迴圈
切成好幾個迴圈跑
等待時間，之後繼續跑迴圈

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/20 15:48
# @Author  : crrlxx
# @Site    : 
# @File    : bankdyy.py
# @Software: PyCharm

import requests
import time
import datetime
import requests
import sys
import lxml.etree as etree
import os
import json
import urllib
import urllib.request
import openpyxl.workbook as workbook

#reload(sys)
#sys.setdefaultencoding("utf-8")

day_now = datetime.date.today()
day7_bef = str(datetime.date.today() - datetime.timedelta(7))
print(day_now, day7_bef)

#ios
#homepath = '/Users/timyan/Desktop/'
#windows
homepath = os.getcwd()
wb_out = workbook.Workbook(homepath+"out.xlsx")
ws_out = wb_out.create_sheet("out")
wb_out.save("out.xlsx")

dict_code = {'CYCC000': '国债', 'CYCC021': '政策性金融债（国开）',
             'CYCC82A': '中期票据AAA+', 'CYCC82B': '中期票据AAA', 'CYCC82C': '中期票据AAA-', 'CYCC82D': '中期票据AA+',
             'CYCC81A': '短期融资券AAA+', 'CYCC81B': '短期融资券AAA', 'CYCC81C': '短期融资券AAA-', 'CYCC81D': '短期融资券AA+',
             'CYCC41A': '同业存单AAA+', 'CYCC41B': '同业存单AAA', 'CYCC41C': '同业存单AA+',
             'CYCC80A': '企业债AAA+', 'CYCC80B': '企业债AAA', 'CYCC80D': '企业债AA+'}


def cbk(a,b,c):
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per=100.0*a*b/c
    if per>100:
        per=100
    print('%.2f%%' % per)


def getshibor():
    # shibor def
    # {"head":{"version":"2.0","provider":"CWAP","req_code":"","rep_code":"200","rep_message":"","ts":1548040200660,"producer":""},"data":{"showDateEN":"21/01/2019 11:00","showDateCN":"2019-01-21 11:00"},"records":[{"termCode":"O/N","shibor":"2.2400","shibIdUpDown":"6.15","shibIdUpDownNum":6.1500000000,"termCodePath":"O/N"},{"termCode":"1W","shibor":"2.5940","shibIdUpDown":"2.40","shibIdUpDownNum":-2.4000000000,"termCodePath":"1W"},{"termCode":"2W","shibor":"2.6370","shibIdUpDown":"7.90","shibIdUpDownNum":7.9000000000,"termCodePath":"2W"},{"termCode":"1M","shibor":"2.7860","shibIdUpDown":"0.90","shibIdUpDownNum":0.9000000000,"termCodePath":"1M"},{"termCode":"3M","shibor":"2.9150","shibIdUpDown":"0.30","shibIdUpDownNum":-0.3000000000,"termCodePath":"3M"},{"termCode":"6M","shibor":"3.0550","shibIdUpDown":"0.60","shibIdUpDownNum":-0.6000000000,"termCodePath":"6M"},{"termCode":"9M","shibor":"3.2410","shibIdUpDown":"0.70","shibIdUpDownNum":-0.7000000000,"termCodePath":"9M"},{"termCode":"1Y","shibor":"3.3000","shibIdUpDown":"0.20","shibIdUpDownNum":-0.2000000000,"termCodePath":"1Y"}]}
    shibor_url = 'http://www.chinamoney.com.cn/r/cms/www/chinamoney/data/shibor/shibor.json'
    fp_html = requests.get(shibor_url).text
    fp_json = json.loads(fp_html)
    print(fp_json['records'][0]["shibor"])


def loadexcel(code):
    base_url = 'http://www.chinamoney.com.cn/dqs/rest/cm-u-bk-currency/ClsYldCurvHisExcel?lang=CN&bondType='
    sdate = '&reference=1&startDate='
    edate = '&endDate='
    end_url = '&termId=0.5'

    try:
        print('Begin download excel:'+dict_code[code])
        #python3
        urllib.request.urlretrieve(base_url + code + sdate + day7_bef + edate + str(day_now) + end_url, homepath + os.sep + code + '.xlsx', cbk)
        #python2
        #urllib.urlretrieve(base_url + code + sdate + day7_bef + edate + str(day_now) + end_url, homepath +os.sep+ code + '.xlsx', cbk)
    except Exception as e:
        print("Download file failed:")
        print(e)

    # except Exception, e:
    #    print e


#国债 CYCC000 0.25 0.5 0.75 1.0 1.5 2.0
#http://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/ClsYldCurvHis?lang=CN&bondType=CYCC000&reference=1&startDate=2019-01-13&endDate=2019-01-20&termId=0.5
#政策性金融债（国开） CYCC021 0.25 0.5 0.75 1.0 1.5 2.0
#http://www.chinamoney.com.cn/dqs/rest/cm-u-bk-currency/ClsYldCurvHisExcel?lang=CN&bondType=CYCC021&reference=1&startDate=2019-01-13&endDate=2019-01-20&termId=0.5
#中期票据AA+(CYCC82D) AAA-(CYCC82C) AAA(CYCC82B) AAA+(CYCC82A) 0.25 0.5 0.75 1.0 1.5 2.0
#http://www.chinamoney.com.cn/dqs/rest/cm-u-bk-currency/ClsYldCurvHisExcel?lang=CN&bondType=CYCC82A&reference=1&startDate=2018-12-18&endDate=2019-01-18&termId=0.5
#短期融资券 AA+(CYCC81D) AAA-(CYCC81C) AAA(CYCC81B) AAA+(CYCC81A)
#企业债 AA+(CYCC80D) AAA(CYCC80B) AAA+(CYCC80A)
#同业存单 AA+(CYCC41C)  AAA(CYCC41B) AAA+(CYCC41A)


if __name__ == '__main__':
    getshibor()
    for item in dict_code.keys():
        loadexcel(item)


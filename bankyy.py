#.*-coding:utf-8-*-
import requests
import time
import datetime
import requests
import sys
import lxml.etree as etree
import json
import urllib
import openpyxl.workbook as workbook

reload(sys)
sys.setdefaultencoding("utf-8")

day_now = datetime.date.today()
day7_bef = str(datetime.date.today() - datetime.timedelta(25))
print day_now, day7_bef

homepath = '/Users/timyan/Desktop/'
shibor_url = 'http://www.chinamoney.com.cn/r/cms/www/chinamoney/data/shibor/shibor.json'
fp_html = requests.get(shibor_url).text
fp_json = json.loads(fp_html)

print fp_json['records'][0]["shibor"]

#shibor def
#{"head":{"version":"2.0","provider":"CWAP","req_code":"","rep_code":"200","rep_message":"","ts":1548040200660,"producer":""},"data":{"showDateEN":"21/01/2019 11:00","showDateCN":"2019-01-21 11:00"},"records":[{"termCode":"O/N","shibor":"2.2400","shibIdUpDown":"6.15","shibIdUpDownNum":6.1500000000,"termCodePath":"O/N"},{"termCode":"1W","shibor":"2.5940","shibIdUpDown":"2.40","shibIdUpDownNum":-2.4000000000,"termCodePath":"1W"},{"termCode":"2W","shibor":"2.6370","shibIdUpDown":"7.90","shibIdUpDownNum":7.9000000000,"termCodePath":"2W"},{"termCode":"1M","shibor":"2.7860","shibIdUpDown":"0.90","shibIdUpDownNum":0.9000000000,"termCodePath":"1M"},{"termCode":"3M","shibor":"2.9150","shibIdUpDown":"0.30","shibIdUpDownNum":-0.3000000000,"termCodePath":"3M"},{"termCode":"6M","shibor":"3.0550","shibIdUpDown":"0.60","shibIdUpDownNum":-0.6000000000,"termCodePath":"6M"},{"termCode":"9M","shibor":"3.2410","shibIdUpDown":"0.70","shibIdUpDownNum":-0.7000000000,"termCodePath":"9M"},{"termCode":"1Y","shibor":"3.3000","shibIdUpDown":"0.20","shibIdUpDownNum":-0.2000000000,"termCodePath":"1Y"}]}
base_url = 'http://www.chinamoney.com.cn'
str_guozhai = '/dqs/rest/cm-u-bk-currency/ClsYldCurvHisExcel?lang=CN&bondType=CYCC000&reference=1&startDate=2019-01-14&endDate=2019-01-21&termId=0.5'
code_guozhai = 'CYCC000'
f_guozhai = 'guozhai.xlsx'
try:
    urllib.urlretrieve(base_url+str_guozhai, homepath+f_guozhai)
except Exception, e:
    print e

wb_out = workbook.Workbook(homepath+"out.xlsx")
ws_out = wb_out.create_sheet("out")
wb_out.save("out.xlsx")



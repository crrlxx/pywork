#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/17 16:31
# @Author  : crrlxx
# @contact: @gmail.com
# @Site    : 
# @File    : confloader.py
# @Software: PyCharm Community Edition
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read('conf/conf.ini') #另个方法是cf.readfp(fp) fp是已打开的文件对象
# 列出所有sections
sec = cf.sections()
print sec
#列出[TB]下的options
pos = cf.options("TH")
print pos
#直接读取配置值
print cf.get("DB","host")  #不要与字典的get()混淆哦
print cf.get("DB","name")
name_list = cf.get("DB","name")
print name_list[1]
print cf.get("DB","user")
print cf.get("DB","pwd")
print cf.getint("TH","thread") #getint()返回的是整型
print cf.getint("TH","timeout")
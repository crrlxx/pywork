#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/17 15:30
# @Author  : crrlxx
# @contact: @gmail.com
# @Site    : 
# @File    : getEntity.py
# @Software: PyCharm Community Edition
from openpyxl import load_workbook
import re

wb_entity = load_workbook("../data/entitydata.xlsx")
ws_entity_data = wb_entity.get_sheet_by_name('entitydatasheet')
ws_entity_result = wb_entity.get_sheet_by_name('entityresultsheet')


def get_coding(str_input):
    '''
    获取编码格式
    '''
    if isinstance(str_input, unicode):
        return "unicode"
    try:
        str_input.decode("utf8")
        return 'utf8'
    except:
        pass
    try:
        str_input.decode("gbk")
        return 'gbk'
    except:
        pass


def get_max_entity_count(label):
    r_index = 1
    entity_count = 0
    while r_index < ws_entity_result.max_row:
        if ws_entity_result.cell(row=r_index, column=2) == label:
            entity_count += 1
        r_index += 1
    print 'out'
    return entity_count


def find_label_to_entity(label, number):
    r_index = 1
    search_count = 1
    while r_index < ws_entity_result.max_row:
        # 判断标签和查找次数
        if ws_entity_result.cell(row=r_index, column=2).value != label or number != search_count:
            search_count += 1
        else:
            # 找到第number个指定label的entity，跳出循环，返回该entity
            entity = ws_entity_result.cell(row=r_index, column=2).value
            break
        r_index += 1
    return entity


total_row_num = ws_entity_data.max_row
row_index = 1
result_index = 1
# 遍历所有实体，按语句类别分别存储实体类别和实体内容
while row_index < total_row_num:
    # 获取实体标注列值
    cell_value = ws_entity_data.cell(row=row_index, column=2).value
    # 正则匹配出实体标签
    re_entity = re.compile(u'\<([a-z]+)\>([\u4e00-\u9fa5]+)\<\/[a-z]+\>')
    entity_type_test = re_entity.findall(cell_value)
    for i in entity_type_test:
        # 存储实体结果
        # 存储domain到ws_entity_result第一列
        ws_entity_result.cell(row=result_index, column=1).value = ws_entity_data.cell(row=row_index, column=1).value
        # 将实体标签存储到ws_entity_result第二列
        ws_entity_result.cell(row=result_index, column=2).value = i[0]
        # 将实体内容存储到ws_entity_result第三列
        ws_entity_result.cell(row=result_index, column=3).value = i[1]
        result_index += 1
    row_index += 1
    if row_index % 1000 == 0:
        print row_index, '/12000'
wb_entity.save("../data/entitydata.xlsx")

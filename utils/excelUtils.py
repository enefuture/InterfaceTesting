#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import os
import sys
import xlsxwriter
import xlrd
reload(sys)  
sys.setdefaultencoding("utf-8")

def write(LISR_EXCEL = [], file=''):
    if not os.path.isfile(file):
        f = open(file, "w")
        f.close()
        print(u"结果文件不存在，创建文件成功")
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Id")
    worksheet.write(0, 1, "接口名")
    worksheet.write(0, 2, "用例描述")
    worksheet.write(0, 3, "请求方法")
    # worksheet.write(0, 4, "Http方式")
    # worksheet.write(0, 5, "主机域名")
    # worksheet.write(0, 6, "端口号")
    worksheet.write(0, 4, "Url")
    worksheet.write(0, 5, "请求参数")
    worksheet.write(0, 6, "依赖业务参数")
    worksheet.write(0, 7, "抓包返回状态码")
    worksheet.write(0, 8, "测试返回状态码")
    worksheet.write(0, 9, "抓包返回MD5")
    worksheet.write(0, 10, "测试返回MD5")
    worksheet.write(0, 11, "抓包返回Json数据")
    worksheet.write(0, 12, "测试返回Json数据")
    worksheet.write(0, 13, "检查点")
    worksheet.write(0, 14, "错误状态码")
    worksheet.write(0, 15, "错误描述")
    worksheet.write(0, 16, "请求耗时")
    temp = 0
    for i in range(0, len(LISR_EXCEL)):
        for j in LISR_EXCEL[i]:
            worksheet.write(i+1, temp, LISR_EXCEL[i]["Id"])
            worksheet.write(i+1, temp+1, LISR_EXCEL[i]["ApiName"])
            worksheet.write(i+1, temp+2, LISR_EXCEL[i]["CaseDesc"])
            worksheet.write(i+1, temp+3, LISR_EXCEL[i]["Method"])
            # worksheet.write(i+1, temp+4, LISR_EXCEL[i]["Http"])
            # worksheet.write(i+1, temp+5, LISR_EXCEL[i]["Host"])
            # worksheet.write(i+1, temp+6, LISR_EXCEL[i]["Port"])
            worksheet.write(i+1, temp+4, LISR_EXCEL[i]["Url"])
            worksheet.write(i+1, temp+5, str(LISR_EXCEL[i]["Param"]))
            worksheet.write(i+1, temp+6, str(LISR_EXCEL[i]["PassParam"]))
            worksheet.write(i+1, temp+7, LISR_EXCEL[i]["Code"])
            worksheet.write(i+1, temp+8,LISR_EXCEL[i]["TestCode"])
            worksheet.write(i+1, temp+9, LISR_EXCEL[i]["Md5"])
            worksheet.write(i+1, temp+10, LISR_EXCEL[i]["TestMd5"])
            worksheet.write(i+1, temp+11, str(LISR_EXCEL[i]["Response"]))
            worksheet.write(i+1, temp+12, str(LISR_EXCEL[i]["TestData"]))
            worksheet.write(i+1, temp+13, str(LISR_EXCEL[i]["CheckPoint"]))
            worksheet.write(i+1, temp+14, str(LISR_EXCEL[i]["Error"]))
            worksheet.write(i+1, temp+15, str(LISR_EXCEL[i]["Msg"]))
            worksheet.write(i+1, temp+16, str(LISR_EXCEL[i]["Time"]))
            break
    workbook.close()

def write_for_fiddler(LISR_EXCEL = [], file=''):
    if not os.path.isfile(file):
        f = open(file, "w")
        f.close()
        print  file + "文件不存在，创建文件成功"
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Id")
    worksheet.write(0, 1, "Date")
    worksheet.write(0, 2, "ApiName")
    worksheet.write(0, 3, "CaseDesc")
    worksheet.write(0, 4, "Method")
    worksheet.write(0, 5, "Http")
    worksheet.write(0, 6, "Host")
    worksheet.write(0, 7, "Port")
    worksheet.write(0, 8, "Path")
    worksheet.write(0, 9, "Query")
    worksheet.write(0, 10, "Param")
    worksheet.write(0, 11, "PassParam")
    worksheet.write(0, 12, "Code")
    worksheet.write(0, 13, "Md5")
    worksheet.write(0, 14, "Response")
    worksheet.write(0, 15, "CheckPoint")
    temp = 0
    CaseDesc = "填写此测试用例的说明，如测试目的，测试是正常请求还是异常请求"
    for i in range(0, len(LISR_EXCEL)):
        for j in LISR_EXCEL[i]:
            worksheet.write(i+1, temp, LISR_EXCEL[i]["Id"])
            worksheet.write(i+1, temp+1, LISR_EXCEL[i]["Date"])
            worksheet.write(i+1, temp+2, LISR_EXCEL[i]["ApiName"])
            worksheet.write(i+1, temp+3, CaseDesc)
            worksheet.write(i+1, temp+4, LISR_EXCEL[i]["Method"])
            worksheet.write(i+1, temp+5, LISR_EXCEL[i]["Http"])
            worksheet.write(i+1, temp+6, LISR_EXCEL[i]["Host"])
            worksheet.write(i+1, temp+7, LISR_EXCEL[i]["Port"])
            worksheet.write(i+1, temp+8, LISR_EXCEL[i]["Path"])
            worksheet.write(i+1, temp+9, str(LISR_EXCEL[i]["Query"]))
            worksheet.write(i+1, temp+10, str(LISR_EXCEL[i]["Param"]))
            worksheet.write(i+1, temp+11, str(LISR_EXCEL[i]["PassParam"]))
            worksheet.write(i+1, temp+12, LISR_EXCEL[i]["Code"])
            worksheet.write(i+1, temp+13, LISR_EXCEL[i]["Md5"])
            worksheet.write(i+1, temp+14, str(LISR_EXCEL[i]["Response"]))
            worksheet.write(i+1, temp+15, str(LISR_EXCEL[i]["CheckPoint"]))
            break
    workbook.close()

def read(file= ''):
    SOURCE_EXCEL = []
    if (os.path.exists(file)) == False:
        return SOURCE_EXCEL
    else:
        data = xlrd.open_workbook(file)
        table = data.sheet_by_index(0)
        nrows = table.nrows #行数
        colnames = table.row_values(0) #某一行数据
        for rownum in range(1, nrows):
             row = table.row_values(rownum)
             if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                SOURCE_EXCEL.append(app)
    return SOURCE_EXCEL
#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
__author__ = 'Administrator'
import os
import time
import sys
from conf import config
from http import interface
from utils import excelUtils
from report import report
def http_requests_excel(list_excel):
    for i in range(len(list_excel)):
        for j in list_excel[i]:
            result = interface.request(list_excel[i]["Http"], list_excel[i]["Host"], list_excel[i]["Port"],list_excel[i]["Path"], list_excel[i]["Query"], list_excel[i]["Method"],
                         list_excel[i]["Param"], list_excel[i]["CheckPoint"])
            list_excel[i]['Url'] = result['url']
            list_excel[i]["Error"] = result['error']
            list_excel[i]["TestCode"]  = result['code']
            list_excel[i]["TestMd5"]  = result['md5']
            list_excel[i]["TestData"] = result['data']
            list_excel[i]["Time"]  = result['time']
            list_excel[i]["Msg"] = result['msg']
            break
    return list_excel


#读取配置文件，拿到读写的文件目录
project_name = config.CURRENT_PROJECT_NAME
if not project_name:
	print r"项目名称为空，请检查"
	sys.exit()
if not config.name_in_project():
	print r"config.py配置文件中的PROJECT_ARRAY没有该项目名称：" + project_name
	sys.exit()
source_folder = config.get_source_folder()
result_folder = config.get_result_folder()

#收集处理结果，邮件展示
total_file = 0
success_file = 0
fail_file = 0
fail_file_name = {}
total_data = []
start_time = time.time()
for parent,dirname,filenames in os.walk(source_folder):
	for filename in filenames:
		full_file_name = os.path.join(parent,filename)
		file_type = filename.split('.')[-1]
		if file_type == 'xlsx':
			total_file = total_file + 1
			try:
				# print r"开始读入excel数据,文件路径：" + full_file_name
				file_data = excelUtils.read(full_file_name)
				# print r"请求对应的API接口"
				data = http_requests_excel(file_data)
				total_data.extend(data)
				write_excel_name = filename.replace('.xlsx','_result.xlsx')
				write_excel_full_path = result_folder + "\\" + write_excel_name
				# print r"开始写入excel数据,文件路径：" +  write_excel_full_path
				excelUtils.write(file_data,write_excel_full_path)
				# print write_excel_full_path + r"文件写入完成"
				success_file = success_file + 1
			except Exception,e:
				fail_file_name[full_file_name] = e
				fail_file = fail_file + 1 

print "共" + str(total_file) + "个文件,成功写入" + str(success_file) + "个文件，失败了" + str(fail_file) + "个文件"
if fail_file_name:
	print r"失败文件如下："
	for filename in fail_file_name:
		print r"失败文件：" + filename + r"失败原因："+ str(fail_file_name[filename])

try:
	report_path = report.produce_report(total_data,start_time)
	print "测试报告在"+ report_path +"中，请查看"
except Exception,e:
	print "生成测试报告失败,失败原因：" + str(e)

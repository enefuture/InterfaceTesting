#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8
import os
import sys
import json
import time
from report import report
from conf import config
from http import interface
from utils import jsonUtils
from utils import excelUtils


LISTDATA = {}

def deal_business(business_logic = []):
	if business_logic:
		for i in range(len(business_logic)):
			result = {
				"error":4,
				"code":0,
				"data":{},
				"md5":'',
				"time":0,
				"msg":"",
				"url":"",
			}
			if business_logic[i]['PassParam'] == '' or business_logic[i]['PassParam'] == "{}":
				result = interface.request(business_logic[i]["Http"], business_logic[i]["Host"], business_logic[i]["Port"],business_logic[i]["Path"],business_logic[i]["Query"], business_logic[i]["Method"],
                         business_logic[i]["Param"], business_logic[i]["CheckPoint"])
				LISTDATA[int(business_logic[i]["Id"])] = result['data']
			elif jsonUtils.is_json(business_logic[i]['PassParam']):
				if jsonUtils.is_json(business_logic[i]['Param']):
					param = json.loads(business_logic[i]['Param'])
					passParam = json.loads(business_logic[i]['PassParam'])
					check_exist = True
					for key in passParam:
						interface_id = passParam[key]['id']
						key_string = passParam[key]['keySet']
						key_list = key_string.split('->')
						pass_data = json.loads(LISTDATA[int(interface_id)])
						for value in key_list:
							if isinstance(pass_data , dict):
								if value in pass_data.keys():
									param[key] = pass_data[value]
									pass_data = pass_data[value]
								else:
									result['msg'] = "PassParam 中的{ '" + key + "':{ 'id':" + str(interface_id) +",'keySet':'"+key_string+"'} 在第" +str(interface_id) +"条测试的返回结果中无该变量"
									check_exist = False
									break
							elif isinstance(pass_data, list):
								length = len(pass_data)
								if isinstance(value,int) and value > 0 and value < length:
									param[key] = pass_data[value]
									pass_data = pass_data[value]
								else:
									result['msg'] = "PassParam 中的{ '" + key + "':{ 'id':" + str(interface_id) +",'keySet':'"+key_string+"'} 在第" +str(interface_id) +"条测试的返回结果中无该变量"
									check_exist = False
									break
					if check_exist:
						business_logic[i]["Param"] = json.dumps(param)
						result = interface.request(business_logic[i]["Http"], business_logic[i]["Host"], business_logic[i]["Port"],business_logic[i]["Path"],business_logic[i]["Query"], business_logic[i]["Method"],
                        business_logic[i]["Param"], business_logic[i]["CheckPoint"])
				else:
					result['msg'] = "Param 必须是Json格式"
			else:
				result['msg'] = "PassParam 不是Json格式"
			business_logic[i]["Url"] = result['url']
			business_logic[i]["Error"] = result['error']
			business_logic[i]["TestCode"]  = result['code']
			business_logic[i]["TestMd5"]  = result['md5']
			business_logic[i]["TestData"] = result['data']
			business_logic[i]["Time"]  = result['time']
			business_logic[i]["Msg"] = result['msg']

		return business_logic
	else:
		print "excel测试源文件为空"
		exit()

def isset(v):
	try:
		type (eval(v))
	except:
		return 0
	else:
		return 1

#读取配置文件，拿到读写的文件目录
project_name = config.CURRENT_PROJECT_NAME
if not project_name:
	print r"项目名称为空，请检查"
	sys.exit()
if not config.name_in_project():
	print r"config.py配置文件中的PROJECT_ARRAY没有该项目名称：" + project_name
	sys.exit()
source_folder = config.get_source_folder(2)
result_folder = config.get_result_folder(2)

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
			# try:
			print r"读取业务文件:" + full_file_name
			file_data = excelUtils.read(full_file_name)
			print r"开始处理业务接口"
			data = deal_business(file_data)
			total_data.extend(data)
			write_excel_name = filename.replace('.xlsx','_result.xlsx')
			write_excel_full_path = result_folder + "\\" + write_excel_name
			print r"开始写入excel数据,文件路径：" +  write_excel_full_path
			excelUtils.write(file_data,write_excel_full_path)
			print write_excel_full_path + r"文件写入完成"
			success_file = success_file + 1
			# except Exception,e:
			# 	fail_file_name[full_file_name] = e
			# 	fail_file = fail_file + 1 

print "共" + str(total_file) + "个文件,成功写入" + str(success_file) + "个文件，失败了" + str(fail_file) + "个文件"
if fail_file_name:
	print "失败文件如下："
	for filename in fail_file_name:
		print "失败文件：" + filename + " 失败原因："+ str(fail_file_name[filename])

try:
	report_path = report.produce_report(total_data,start_time,2)
	print "测试报告在"+ report_path +"中，请查看"
except Exception,e:
	print "生成测试报告失败,错误原因：" + str(e) 

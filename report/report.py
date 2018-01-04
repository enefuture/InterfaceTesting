#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import os
import time
import sys
import json
sys.path.append('../')
from conf import config
reload(sys)
sys.setdefaultencoding('utf-8')
# data: [%(error0_count)s, %(error1_count)s, %(error2_count)s, %(error3_count)s, %(error4_count)s]
def deal_total_data(total_data):
	interface_status = {
		0:[],
		1:[],
		2:[],
		3:[],
		4:[]
	}
	if isinstance(total_data,list):
		for data in total_data:
			interface_status[data['Error']].append(data)
	else:
		print r"错误：总数据类型不为list"
	return interface_status

#source_type = 1 是单接口源文件目录  source_typ = 2 是业务接口源文件
def produce_report(total_data,start_time,source_type = 1):
	project_info = {
		'项目名称' : config.CURRENT_PROJECT_NAME,
		'测试耗时' :'',
		'接口域名' : config.PROJECT_DOMIN[config.CURRENT_PROJECT_NAME],
		'测试总览' : ''
	}
	error_status_info = {
		0:'请求成功',
		1:'请求失败',
		2:'未通过检查点',
		3:'数据格式错误',
		4:'参数错误',
	}
	error_info = ['请求成功','请求失败','未通过检查点','数据格式错误','参数错误']
	bar_chart_count = []
	pie_chart_count = []
	error_list = []
	if total_data:
		total_count = len(total_data)
		divide_by_error = deal_total_data(total_data)
		for status in divide_by_error:
			bar_chart_count.append(len(divide_by_error[status]))
			pie_chart_count.append({'value':len(divide_by_error[status]),'name':error_status_info[status]})
			if status != 0:
				error_list.extend(divide_by_error[status])
		error_count = total_count - len(divide_by_error[0])
		project_info['测试总览'] = "共"+ str(total_count) + "个接口，成功" + str(len(divide_by_error[0]))+"个接口，失败"+ str(error_count) + "个接口"
		project_info['测试耗时'] = time.time() - start_time
		data = {
			'project_info': project_info,
			'error_info' : error_info,
			'bar_chart_count' : bar_chart_count,
			'pie_chart_count' : pie_chart_count,
			'error_list' : error_list
		}
		# return type(data)
		# error_list = str(error_list)
		# error_list = json.dumps(error_list,ensure_ascii=False)
		# return json.loads(error_list)
		data = json.dumps(data, ensure_ascii=False)
		result = {'data':data}
		path = os.getcwd() + "\\report\\report_template.html"
		report_template_html = open(path,'r').read()
		report = report_template_html % result
		current_time = time.strftime("%Y-%m-%d",time.localtime(time.time()))
		write_html_path = os.getcwd() + "\\" + config.DATA_PATH + "\\" + config.CURRENT_PROJECT_NAME
		if source_type == 1:
			write_html_path = write_html_path + "\\singleInterface\\report_" + current_time + ".html" 
		else:
			write_html_path = write_html_path + "\\business\\report_" + current_time + ".html"
		report_html = open(write_html_path,'w')
		report_html.write(report)
		report_html.close()
		return write_html_path
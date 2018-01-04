#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import os
import sys
import urllib
import urllib2
import json
import re
sys.path.append("..")
import httpBase
from utils import checkUtils
from utils import jsonUtils
reload(sys)  
sys.setdefaultencoding("utf-8")

'''获取返回后的数据，根据检查点check_point判断返回结果是否正确
	error 状态码说明
	：0  请求成功，返回数据正常
	：1  请求失败，code 状态码大于200
	：2  请求成功，返回数据状态,格式与CheckPoint中不一致
		 包括：返回数据的error状态码与CheckPoint中不一致
		 返回数据格式与CheckPoint中不一致，不为空，数量不匹配等，具体看检查点配置
	：3  返回数据不为Json格式，无法解析
	: 4  参数错误，请检查相应参数
'''

user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}

def request(http='http://', host='',port="",path='',query = '{}',method = 'GET',values = '{}',check_point = '{}',headers = {}):
	result = {
		"url":"",
		"error":1,
		"code":0,
		"md5":"",
		"data":{},
		"time":0,
		"msg":"",
		}
	# check_point = json.dumps(check_point)
	# values = json.dumps(values)
	if port.strip() == '':
		url = http + host + path 
	elif port.isdigit():
		url = http + host+ ":" + port + path
	else:
		result['msg'] = "端口号port格式错误"
		result['error'] = 4
		return result
	if  not jsonUtils.is_json(query):
		result['msg'] = "Query 必须是Json格式"
		result['error'] = 4
		return result
	if  not jsonUtils.is_json(values):
		result['msg'] = "Param 必须是Json格式"
		result['error'] = 4
		return result
	if not jsonUtils.is_json(check_point):
		result['msg'] = "CheckPoint 必须是Json格式"
		result['error'] = 4
		return result
	query = json.loads(query)
	query_string = urllib.urlencode(query)
	url = url + '?' + query_string
	print url
	result = httpBase.request(url,headers,method,values)
	#要在请求后才可以给其赋值
	result['md5'] = ''
	result['url'] = url
	check_point_json = eval(check_point)
	# 将带有md5的json串格式化，提取Md5和json串
	md5_string = re.match('^\w+',result['data'])
	if md5_string:
		md5_string = md5_string.group()
		result['md5'] = md5_string
		result_string = result['data'].split(md5_string)[-1]
		# print result_string
		# result_json = json.dumps(result_string,ensure_ascii=False)
		result_json = json.loads(result_string)
		result['data'] = json.dumps(result_json,ensure_ascii=False,sort_keys=True)
	else:
		if result['data'].startswith('{'):
			result_json = json.loads(result['data'])
			result['data'] = json.dumps(result_json,ensure_ascii=False,sort_keys=True)
		else:
			result_json = json.dumps(result['data'],ensure_ascii=False,sort_keys=True)
			result_json = json.loads(result_json)
			result['data'] = result_json
	# print result_json
	# print check_point_json
	# 这里可以做数据解析，根据是否成功请求和相应的检查点确定接口返回数据是否成功
	if result['error'] == 1 or result['error'] == 3:
		return result
	elif not check_point_json:
		result['msg'] = "检查点为空，不需检查"
	elif not result['data'] and check_point_json:
		result['msg'] = "返回数据为空，与检查点不匹配"
		result['error'] = 2
	else:
		# result['data'] = json.dumps(result_json,ensure_ascii=False)
		for check_key in check_point_json:
			if check_key in result_json:
				check_result = checkUtils.check_data(check_key,check_point_json[check_key],result_json[check_key])
				result['error'] = check_result['error']
				if check_result['msg']:
					result['msg'] = check_result['msg']
					break
			else:
				result['error'] = 2
				result['msg'] = "返回数据格式与CheckPoint格式不一致,无"+check_key+"字段"
				break
	return result

# url = "api.app.tvfanqie.com/mandroid/channel/home?ss=-1&token=d7aae496bce0855c4f8be21bbbffdbdc&ver=1&ch=&debug=1"
# check_point = {'error':0,'msg':'ok','data':'>14'}
# # # check_point = json.dumps(str(check_point))
# # # check_point = jsonUtils.is_json(str(check_point))
# data = request('http://',url,check_point = str(check_point))
# print data
# print json.dumps(data['msg'],ensure_ascii=False)

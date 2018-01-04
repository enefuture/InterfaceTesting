#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import types
import re
import sys
reload(sys)  
sys.setdefaultencoding("utf-8")

#标记那些比较符可用
FLAG = ['=','>','<']
def check_data(check_key,check_point_data = '',return_data = ''):
	result = {
		'error' : 2,
		'msg' :''
	}
	if check_point_data == return_data:
		result['error'] = 0
	elif type(check_point_data) is types.StringType:
		check_point_data = check_point_data.upper()
		if type(return_data) is types.StringType:
			return_data = return_data.upper()
		if check_point_data =='' or check_point_data == 'NULL':
			result['error'] = 0
		elif check_point_data == 'NOT NULL':
			if return_data:
				result['error'] = 0
			else:
				result['msg'] = r'错误：检查点要求 '+check_key+' 字段返回不能为空，返回数据错误'
		elif isinstance(return_data,list):
			length = len(return_data)
			result['msg'] = length
			num_arr = re.findall('\d+',check_point_data)
			if num_arr and len(num_arr) == 1:
				num = num_arr[0]
				equal = re.match('=',check_point_data)
				greater = re.match('>',check_point_data)
				less = re.match('<',check_point_data)
				if equal:
					if num == length:
						result['error'] = 0
					else:
						result['msg'] = r"错误：配置检查点的key:"+check_key+"的数量"+str(num)+"等于返回的key:"+check_key+"的值:"+str(length)+"，实际结果不相等"
				elif greater:
					if length > num:
						result['error'] = 0
					else:
						result['msg'] = r"错误：配置检查点的key:"+check_key+"的数量"+str(num)+"大于返回的key:"+check_key+"的值:"+str(length)+"，实际结果不大于"
				elif less:
					if length < num:
						result['error'] = 0
					else:
						result['msg'] = r"错误：配置检查点的key:"+check_key+"的数量"+str(num)+"小于返回的key:"+check_key+"的值:"+str(length)+"，实际结果不小于"
				else:
					result['msg'] = r"错误：检查点格式有误，请查证key:"+check_key+"是否为= 数字，> 数字，< 数字"
			else:
				result['msg'] = r"错误：检查点格式有误，请查证key:"+check_key+"是否为= 数字，> 数字，< 数字"
		else:
			result['msg'] = r"错误：检查点格式有误，请查证key:"+check_key+"是否为= 数字，> 数字，< 数字，NULL，NOT NULL"
			result['error'] = 2
	elif type(check_point_data) is types.IntType :
		return_data = int(return_data)
		if check_point_data == return_data:
			result['error'] = 0
		else:
			result['msg'] = r'错误：检查点要求返回的'+str(check_key)+'的值:'+str(return_data)+'不等于检查点'+str(check_key)+'的值：'+str(check_point_data)
	return result
	
def compare(operation = '', length = 0, num = 0):
	if operation == '=':
		return length == num
	elif operation == '>':
		return length > num
	elif operation == '<':
		return length < num
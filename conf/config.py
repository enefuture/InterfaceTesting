#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import os
import time
DATA_PATH = "data"

FIDDLER_FILTER_PATH = "D:\\FiddlerFilterApi"

CURRENT_PROJECT_NAME = "Pop"

PROJECT_ARRAY = ["Pop"]

PROJECT_DOMIN = {
	'Pop':['api.test1.com',,'api.test2.com'],
} 

def create_fiddler_folder():
	try:
		if not os.path.isdir(FIDDLER_FILTER_PATH):
			os.makedirs(FIDDLER_FILTER_PATH)
		current_time = time.strftime("%Y-%m-%d",time.localtime(time.time()))
		project_folder = FIDDLER_FILTER_PATH + "\\" + CURRENT_PROJECT_NAME + "_" + current_time
		if not os.path.isdir(project_folder):
			os.makedirs(project_folder)
		if name_in_project:
			api_folder = PROJECT_DOMIN[CURRENT_PROJECT_NAME]
			print api_folder
			for key in api_folder:
				project_path = project_folder + "\\" + key
				if not os.path.isdir(project_path):
					os.makedirs(project_path)
	except Exception,e:
		print "文件系统不支持，异常信息：" + str(e)

def create_project_folder():
	for project_name in PROJECT_ARRAY:
		project_folder_name = os.getcwd() + "\\" + DATA_PATH + "\\" + project_name
		if not os.path.isdir(project_folder_name):
			os.makedirs(project_folder_name)
		folder_dict = {
			"single_interface_folder": project_folder_name + "\\singleInterface",
			"business_folder" : project_folder_name + "\\business"
		}
		for folder in folder_dict:
			if not os.path.isdir(folder_dict[folder]):
				os.makedirs(folder_dict[folder])
				source_folder = folder_dict[folder] + "\\source"
				result_folder = folder_dict[folder] + "\\result"
				if not os.path.isdir(source_folder):
					os.makedirs(source_folder)
				if not os.path.isdir(result_folder):
					os.makedirs(result_folder)


def get_project_domin():
	if CURRENT_PROJECT_NAME in PROJECT_DOMIN:
		return PROJECT_DOMIN[CURRENT_PROJECT_NAME]
	return False

#source_type = 1 是单接口源文件目录  source_typ = 2 是业务接口源文件
def get_source_folder(source_type = 1):
	if source_type == 1 :
		source_folder = '\\singleInterface'
	elif source_type == 2:
		source_folder = "\\business"
	else:
		print r"读文件源类型错误"
		sys.exit()
	source_folder = os.getcwd() + "\\" + DATA_PATH + "\\" + CURRENT_PROJECT_NAME + source_folder + "\\source"
	if os.path.isdir(source_folder):
		return source_folder
	return False
#source_type = 1 是单接口源文件目录  source_typ = 2 是业务接口源文件
def get_result_folder(result_type = 1):
	if result_type == 1 :
		result_folder = '\\singleInterface'
	elif result_type == 2:
		result_folder = "\\business"
	else:
		print r"读文件源类型错误"
		sys.exit()
	result_folder = os.getcwd() + "\\" + DATA_PATH + "\\" + CURRENT_PROJECT_NAME + result_folder + "\\result"
	if os.path.isdir(result_folder):
		return result_folder
	return False

def name_in_project():
	if CURRENT_PROJECT_NAME in PROJECT_ARRAY:
		return True
	return False

def init():
	create_project_folder()
	create_fiddler_folder()

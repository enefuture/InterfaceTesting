#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import os
import ConfigParser
import sys
from conf import config
from utils import fiddlerUtils
from utils import excelUtils
reload(sys)
sys.setdefaultencoding('utf-8')

#读取配置文件
project_name = config.CURRENT_PROJECT_NAME
if not project_name:
	print r"项目名称为空，请检查"
	sys.exit()
if not config.name_in_project():
	print r"config.py配置文件中的PROJECT_ARRAY没有该项目名称：" + project_name
	sys.exit()

source_folder = config.get_source_folder()

fiddler_filter_path = config.FIDDLER_FILTER_PATH + "\\" + project_name
read_folder_name = config.get_project_domin()
print read_folder_name
if not read_folder_name:
	print r"config.py配置文件中的PROJECT_DOMIN的读取文件数组为空，或不存在该项目，请检查"
	sys.exit()

#收集处理结果
total_file = 0
success_file = 0
fail_file = 0
fail_file_name = []
#从配置域名文件夹中读取数据
if read_folder_name:
	for folder_name in read_folder_name:
		folder_name = fiddler_filter_path + "\\" + folder_name
		if os.path.exists(folder_name):
			for parent,dirname,filenames in os.walk(folder_name):
				for filename in filenames:
					full_file_name = os.path.join(parent,filename)
					file_type = filename.split('.')[-1]
					if file_type == 'txt':
						total_file = total_file + 1
						try:
							#读取文件类型为txt格式的fiddler过滤的接口数据
							file_data = fiddlerUtils.read_fiddler(full_file_name)
							write_excel_name = filename.replace('.txt','.xlsx')
							write_excel_full_path = source_folder + "\\" + write_excel_name
							print full_file_name + r"读取完毕，下面开始写入excel源数据文件"
							excelUtils.write_for_fiddler(file_data,write_excel_full_path)
							print write_excel_full_path + r"写入完成"
							success_file = success_file + 1
						except Exception,e:
							fail_file_name.append(full_file_name)
							fail_file = fail_file + 1 
		else:
			print "不存在" + folder_name + "目录"
print "共" + str(total_file) + "个文件,成功写入" + str(success_file) + "个文件，失败了" + str(fail_file) + "个文件"
if fail_file_name:
	print "失败文件如下："
	for fail in fail_file_name:
		print fail 





#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
## FileName ReadSessions.py
# Author: HeyNiu
# Created Time: 20160729
"""
读取录制的所有接口信息
"""
import os
import sys
import json
import codecs
import re
import urlparse
reload(sys)
sys.setdefaultencoding( "utf-8" )

def init_single_session():
    single_session = {
        'Date' : '',
        'Id' : '',
        'ApiName' : '',
        'Method' : '',
        'Http' : '',
        'Host' : '',
        'Port' : '',
        'Path' : '',
        'Query': {},
        'Param' : {},
        'PassParam' : {},
        'Code':'',
        'Md5' : '',
        'Response': {},
        'CheckPoint':{}
    }
    return single_session

def read_fiddler(path):
    single_session = init_single_session()
    total_session = []
    try:
        fiddler_log = codecs.open(path, 'r', encoding='utf-8').readlines()
    except UnicodeDecodeError:
        fiddler_log = codecs.open(path, 'r',encoding='utf-16-le').readlines()
    for i1 in fiddler_log:
        try:
            if not i1.startswith("\n"):
                if i1.startswith("Request date:"):
                    single_session['Date'] = i1.split("Request date: ")[-1].strip("\n").strip('\r')
                elif i1.startswith("Request http:"):
                    single_session['Http'] = i1.split("Request http: ")[-1].strip("\n").strip('\r')
                elif i1.startswith("Request url: "):
                    url = i1.split("Request url: ")[-1].strip("\n").strip('\r')
                    url_arr = url.split("/",1)
                    single_session['Host'] = url_arr[0]
                elif i1.startswith("Request header: "):
                    header = i1.split("Request header: ")[-1]
                    header = header.split(" ")
                    single_session['Method'] = header[0]
                    url = urlparse.urlparse(header[1])
                    single_session['Path'] = url.path
                    query_dict = urlparse.parse_qs(url.query,True)
                    if query_dict != "":
                        for query_key in query_dict:
                            query_string = ''
                            max_index = len(query_dict[query_key]) - 1
                            for i in range(len(query_dict[query_key])):
                                if i == max_index:
                                    query_string = query_string + str(query_dict[query_key][i])
                                else:
                                    query_string = query_string + str(query_dict[query_key][i]) + ','
                            query_dict[query_key] = query_string
                    single_session['Query'] = json.dumps(query_dict,ensure_ascii=False)
                elif i1.startswith("Request body: "):
                    param_string = i1.split("Request body: ")[-1].strip("\n").strip('\r')
                    if param_string:
                        param_string = param_string.split('&')
                        if param_string:
                            for parse_param in param_string:
                                parse_param = parse_param.split('=')
                                single_session['Param'][str(parse_param[0])] = str(parse_param[1])
                        else:
                            parse_param = param_string.split('=')
                            single_session['Param'][str(parse_param[0])] = str(parse_param[1])
                    else:
                        single_session['Param'] = {}
                elif i1.startswith("Response code: "):
                    single_session['Code'] = i1.split("Response code: ")[-1].strip("\n").strip('\r')
                elif i1.startswith("Response body: "):
                    response_body = i1.split("Response body: ")[-1].strip("\n").strip('\r')
                    md5_string = re.match('^\w+',response_body)
                    if md5_string:
                        md5_string = md5_string.group()
                        single_session['Md5'] = md5_string
                        json_string = response_body.split(md5_string)[-1]
                        json_body = json.loads(json_string)
                        single_session['Response'] = json.dumps(json_body,ensure_ascii=False,sort_keys=True)
                    else:
                        if response_body.startswith('{'):
                            json_body = json.loads(response_body)
                            single_session['Response'] = json.dumps(json_body,ensure_ascii=False,sort_keys=True)
                        else:
                            json_body = json.dumps(response_body,ensure_ascii=False,sort_keys=True)
                            single_session['Response'] = json.loads(json_body)
            if i1.startswith("Session end"):
                total_session.append(single_session)
                single_session = init_single_session()
        except Exception,e:
            print "read file: " + path + "  error"
            print e
    return total_session

# test = read_fiddler("D:\FiddlerFilterApi\Pop\\api.app.tvfanqie.com\\api.app.tvfanqie.com_mandroid_static_welcome.json_SuccessApi.txt")
# print test
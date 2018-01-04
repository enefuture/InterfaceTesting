#!/usr/bin/python  
# -*- coding: utf-8 -*-  
#coding=utf-8  
import os
import sys
import urllib
import urllib2
import socket
import time
import json
import ssl
import cookielib
reload(sys)  
sys.setdefaultencoding("utf-8")
'''
设置代理地址，通过读配置文件的方式
'''
#可以通过配置enable_proxy开启代理
enable_proxy = True
#可以读取配置获取代理地址
proxy_handler = urllib2.ProxyHandler({"http:":'114.244.112.220:8118'})
null_proxy_handler = urllib2.ProxyHandler({})

if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)
#print "设置代理结束"

# # 初始化一个CookieJar来处理Cookie
# cookieJar=cookielib.CookieJar()
# # 实例化一个全局opener
# opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
# urllib2.install_opener(opener)

'''
	请求Url获取相应的数据
    输入参数说明:
        user_agent = 'User-Agent: 360 Video App/3.5.27 Android/5.1.1 QIHU'
        host : 主机名
        uri ：访问的路径
        user-agent：请求头
        values ：请求参数
    输出参数说明：
        error ：0 => 请求成功，1 => 请求失败 NOTNULL
        code ： 请求的状态码   NULL
        data ： 返回的接口数据
        time ： 请求的耗时     NULL
        msg  ： 异常信息       NULL
'''
header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Cookie': "v=IP'^O5rKWm:I(</A`l<K",
    'Upgrade-Insecure-Requests': 1,
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
def request(url='',headers = {},method = 'GET', values=''):
    buf_except_msg = ""
    buf = ""
    code = ""
    try:
        start_time = time.time()
        if headers:
            headers = headers
        else:
            headers = header

        if values == '' or values == '{}':
            data = ''
            req = urllib2.Request(url,headers = headers)
        else:
            data = urllib.urlencode(eval(values))
            req = urllib2.Request(url,data,headers)
        #加入下行代码，避免 “SSL: CERTIFICATE_VERIFY_FAILED” 错误。
        context = ssl._create_unverified_context()
        response = urllib2.urlopen(req,context = context) 
        code = response.getcode()
        if code  == 200:
            buf = response.read()
            response.close()
            info = {'error':0, 'code':code, 'data':buf, 'time':time.time()-start_time, 'msg':'请求成功'}
            return info
            # buf_array = json.loads(buf)
            # if buf_array['error'] == 0:
            #     print "请求成功","时间："+  str(time.time()-start_time)+"s "
        else:
            #可以打log
            print "请求失败","状态返回码" + str(code)
            info = {'error':1, 'code':code, 'data':buf, 'time':time.time()-start_time, 'msg':'请求失败'}
            return info
    except  urllib2.URLError,e:
        if hasattr(e,'reason') and hasattr(e,'code'): 
            info = {'error':1, 'code':e.code, 'data':buf, 'time':time.time()-start_time, 'msg':str(e.reason)} 
        elif hasattr(e,'reason'):
            info = {'error':1, 'code':'', 'data':buf, 'time':time.time()-start_time, 'msg':str(e.reason)}
        elif hasattr(e,'code'):
            info = {'error':1, 'code':e.code, 'data':buf, 'time':time.time()-start_time, 'msg':str(e.read())} 
        else:
            info = {'error':1, 'code':0, 'data':buf, 'time':time.time()-start_time, 'msg':'未知错误，可能是链接超时'} 
        return info
    # finally:
    #     if response:
    #         response.close() 





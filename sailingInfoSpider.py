# -*- coding: utf-8 -*-
import random
import os
import subprocess
import re
import requests
import sys
import lxml

from bs4 import BeautifulSoup
from generateExcel import generateExcel
from agentAndProxies import hds
from agentAndProxies import GetIpProxy
from model.elementConstant import elementConstant

class salingInfo:
    # 初始化构造函数
    def __init__(self):
        if len(sys.argv) <= 1:
            print(u'[ERROR] 参数不足，需要城市的拼音，如 beijing')
            exit()
        else:
            self.city = str(sys.argv[1])
            
        # 创建动态 IP 池
        self.getIpProxy = GetIpProxy()
        self.url = "https://bj.lianjia.com/ershoufang/pg{}/"
        # 每套房的各种字段暂存（最终会写入 Excel 或通过 DataFrame 写入本地文件）
        self.infos = {}
        # 代理服务器地址
        self.proxyServer = ()
        # 写入 Excel 的 Column 号与字符串对照常量
        self.elementConstant = elementConstant()
        # 传参使用进行 Excel 生成
        self.generateExcel = generateExcel()
        
        # 检查 url 列表
        # TODO 后面需要根据不同的 url 开启不同 Python 进程
        path = os.path.join(os.getcwd(), u'output', self.city,'url.txt')
        with open(path, 'r') as urlFile:
            allUrls = urlFile.readlines()
            for i in range(0,len(allUrls)):
                url = allUrls[i]
                formattedUrl = url.replace('\n','')
                # print('formattedUrl',formattedUrl)
                self.checkProcessCount(formattedUrl)
        
        

    # 检查 url 对应的房产数据个数是否符合规矩（如果大于 3000，需要重新调整）
    def checkProcessCount(self, url):
        response = self.requestUrlByProxy(url.replace('pg','pg1'))
        print(u'检查 URL：{0}'.format(url))
        # 正则表达式，取出当前 url 会返回多少条结果
        # 因为链家 PC 端，每个 url 最多显示 100 页，每页最多 30 条数据，所以如果返回值大于 3000，则需要重新分拆 url
        # 此时应该暂时中断请求，以免遗漏数据
        partent = re.compile('<h2 class="total fl">.*?<span>\s*(.*?)\s</span>.*?</h2>')
        result = re.findall(partent, response.text)
        if len(result) > 0:
            totalCount = int(result[0])
            if totalCount > 3000:
                print(u'[ERROR] 数据个数：{0} 超过 3000 条，需要重新拆解 url，退出'.format(totalCount))
                exit()
            else:
                if totalCount % 30 > 0:
                    pageCount =  int(totalCount / 30) + 1
                else:
                    pageCount =  int(totalCount / 30)
                print(u'[Success] 数据个数：{0}，分页数：{1}'.format(totalCount, pageCount))
                # woker.py 的文件路径
                workerPyPath = os.path.join(os.getcwd(),'spiderWorker.py')
                #test = 'https://bj.lianjia.com/ershoufang/pg1bp0ep100/'
                partent2 = re.compile('https://.*?/.*?/pg.*?bp(.*?)ep(.*?)/')
                values = re.findall(partent2, url)
                fileExt = u'begin{0}_end{1}'.format(values[0][0],values[0][1])
                # 参数方面：调用 powershell，指向 woker.py 路径，传入聚合 url，个数，页数，目标文件存储位置，城市
                args=[r"powershell", workerPyPath, url, str(totalCount), str(pageCount), fileExt, self.city]
                print(args)
                # 开新进程，执行任务
                p = subprocess.Popen(args, stdout=subprocess.PIPE)
                
        else:
            print(u'解析数据个数失败，退出')
            exit()

    # 封装统一 request 请求，采取动态代理和动态修改 User-Agent 方式进行访问设置，减少服务端手动暂停的问题
    def requestUrlByProxy(self, url):

        try:
            if len(self.proxyServer) == 0:
                tempProxyServer = self.getIpProxy.get_random_ip()
            else:
                tempProxyServer = self.proxyServer

            proxy_dict = {
                tempProxyServer[0]: tempProxyServer[1]
            }
            tempUrl = requests.get(url, headers=hds[random.randint(0, len(hds) - 1)], proxies=proxy_dict)

            code = tempUrl.status_code
            if code >= 200 or code < 300:
                self.proxyServer = tempProxyServer
                return tempUrl
            else:
                self.proxyServer = self.getIpProxy.get_random_ip()
                return self.requestUrlByProxy(url)
        except Exception as e:
            self.proxyServer = self.getIpProxy.get_random_ip()
            s = requests.session()
            s.keep_alive = False
            return self.requestUrlByProxy(url)

spider = salingInfo()
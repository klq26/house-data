# -*- coding: utf-8 -*-
import os
import random
import re
import requests
import sys
import lxml

from agentAndProxies import hds
from agentAndProxies import GetIpProxy
from logger import logger

from model.cityConstant import cityConstant

class urlDetector:
    
    # 初始化构造函数
    def __init__(self):
        # 根据 beijing 生成 bj 本地字典
        if len(sys.argv) <= 1:
            print(u'[ERROR] 参数不足，需要城市的拼音，如 beijing')
            exit()
        else:
            self.city = str(sys.argv[1])
        
        # 各个城市已经准备好的价格区间（保证每个区间页数少于 100）
        self.priceIntervals = {}
        # 城市常量
        self.cityConstant = cityConstant()
        
        # 城市二手房总数
        self.cityCount = 0
        # 创建动态 IP 池
        self.getIpProxy = GetIpProxy()
        # 代理服务器地址
        self.proxyServer = ()
        # 地址模板
        self.url = "https://{0}.lianjia.com/ershoufang/bp{1}ep{2}/"
        # logger 初始化
        self.logger = logger(os.path.join(os.getcwd(),'urlDetector_{0}.log'.format(self.city)))

    # 检查 url 对应的 URL 下究竟有多少条数据，好做进一步拆分
    def checkPriceIntervalCount(self):
        # 常见区间
        #standardIntervals = [0,100,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000,10000]
        if self.city in self.cityConstant.cityPriceIntervals.keys():
            standardIntervals = self.cityConstant.cityPriceIntervals[self.city]
        else:
            standardIntervals = [0,66,100,133,166,200,233,266,300,333,366,400,433,466,500,533,566,600,633,666,700,733,766,800,833,866,900,933,966,1000,1500,2000,3000,4000,5000,10000]
        
        for i in range(1,len(standardIntervals)):
            #print(u'{0} {1}'.format(standardIntervals[i-1],standardIntervals[i]))
            url = self.url.format(self.cityConstant.cityToBref[self.city],standardIntervals[i-1],standardIntervals[i])            
            response = self.requestUrlByProxy(url)
            print(u'检查 URL：{0}'.format(url))
            partent = re.compile('<h2 class="total fl">.*?<span>\s*(.*?)\s</span>.*?</h2>')
            result = re.findall(partent, response.text)
            if len(result) > 0:
                totalCount = int(result[0])
                if totalCount % 30 > 0:
                    pageCount =  int(totalCount / 30) + 1
                else:
                    pageCount =  int(totalCount / 30)
                print(u'[Success] {0}w ~ {1}w 数据个数：{2}，分页数：{3}'.format(standardIntervals[i-1], standardIntervals[i], totalCount, pageCount))
                self.cityCount = self.cityCount + totalCount
                self.logger.log.debug(u'{0}-{1}\t{2}\t{3}'.format(standardIntervals[i-1], standardIntervals[i], totalCount, pageCount))
            else:
                print(u'解析数据个数失败，退出')
                exit()
        print(u'{0} 总数量为：{1}'.format(self.city,self.cityCount))
        self.logger.log.debug(u'{0}'.format(self.cityCount))

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
                #print('return self.requestUrlByProxy(url) 1')
                return self.requestUrlByProxy(url)
        except Exception as e:
            #print(e)
            self.proxyServer = self.getIpProxy.get_random_ip()
            s = requests.session()
            s.keep_alive = False
            #print('return self.requestUrlByProxy(url) 2')
            return self.requestUrlByProxy(url)

urlDetector = urlDetector()
urlDetector.checkPriceIntervalCount()
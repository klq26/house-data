# -*- coding: utf-8 -*-
import random
import re
import os
import requests
import sys
import lxml
import time

from logger import logger
from bs4 import BeautifulSoup
from generateExcel import generateExcel
from agentAndProxies import hds
from agentAndProxies import GetIpProxy
from model.elementConstant import elementConstant
from model.cityConstant import cityConstant

#print ("Start : %s" % time.ctime())
#print ("End : %s" % time.ctime())

class spiderWorker:
    # 初始化构造函数
    def __init__(self):
        self.elementConstant = elementConstant()
        self.cityConstant = cityConstant()
        self.getIpProxy = GetIpProxy()
        self.url = u''
        # debug
        #self.url = 'https://bj.lianjia.com/ershoufang/pinggu/pg/'.replace('pg','pg{0}')
        #self.totalCount = 90
        #self.pageCount = 3
        #self.xlsPathIdentifier = 'pinggu'
        #self.city = 'beijing'
        self.infos = {}
        self.proxyServer = ()
        # 传参使用进行Excel生成
        self.generateExcel = generateExcel()
        self.elementConstant = elementConstant()
        

    # 0）准备工作
    # 获取参数：1：url 2：totalCount 3：pageCount 4：xlsPath 唯一标识 5：城市
    def prepare(self,url,totalCount,pageCount,xlsPathIdentifier,city,taskIndex = 1):
        # 因为 {0} 作为参数无法传过来，所以把 pg 替换为 pg{0}
        self.url = str(url).replace('pg','pg{0}')
        self.totalCount = int(totalCount)
        self.pageCount = int(pageCount)
        self.xlsPathIdentifier = str(xlsPathIdentifier)
        self.city = str(city)
        self.dateFolder = time.strftime("%Y%m", time.localtime())
        self.taskIndex = taskIndex
        # logger 初始化
        self.outputFolder = os.path.join(os.getcwd(), u'output', self.city, self.dateFolder)
        if not os.path.exists(self.outputFolder):
            os.makedirs(self.outputFolder)
        self.logger = logger(os.path.join(self.outputFolder, 'worker_{0}.log'.format(self.xlsPathIdentifier)))
        
    # 1）开始
    def start(self):
        assert self.url != '',u'[ERROR] 应该先调用 prepare 函数进行初始化再使用'
        self.generateExcel.addSheetExcel(u'在售列表')
        for i in self.generate_allurl(self.pageCount):
            self.get_allurl(i)
            self.logger.log.info(i)
        path = os.path.join(self.outputFolder, 'HouseData_{0}.xlsx'.format(self.xlsPathIdentifier))
        self.generateExcel.saveExcel(path)

    # 2）生成需要生成页数的链接
    def generate_allurl(self, pageCount):
        for url_next in range(1, pageCount + 1):
            self.page = url_next
            yield self.url.format(url_next)
    
    # 3）从每个聚合列表页下，获取所有房产卡片数据
    def get_allurl(self, generate_allurl):
        geturl = self.requestUrlForRe(generate_allurl)
        if geturl.status_code == 200:
            # 提取 title 跳转地址　对应每套商品房 SKU
            re_set = re.compile('<div class="item*?".*?<a.*?class="img.*?".*?href="(.*?)"')
            re_get = re.findall(re_set, geturl.text)
            for index in range(len(re_get)):
                self.open_url(re_get[index], index)
                self.logger.log.info(re_get[index])
                # 增加休眠时间，防止服务器拒绝
                #time.sleep(1.5)
                
    # 4）爬取每一套房屋 SKU 的详细数据
    def open_url(self, re_get, index):
        res = self.requestUrlForRe(re_get)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            self.infos[u'网址'] = re_get
            self.infos[u'标题'] = soup.select('.main')[0].text
            self.infos[u'总价'] = soup.select('.total')[0].text
            self.infos[u'每平方售价'] = soup.select('.unitPriceValue')[0].text

            self.infos[u'户型'] = soup.select('.mainInfo')[0].text
            self.infos[u'朝向'] = soup.select('.mainInfo')[1].text
            self.infos[u'大小'] = soup.select('.mainInfo')[2].text
            self.infos[u'楼层'] = soup.select('.subInfo')[0].text
            self.infos[u'装修'] = soup.select('.subInfo')[1].text
            self.infos[u'房子类型'] = soup.select('.subInfo')[2].text
            if self.infos[u'房子类型'] == u'未知':
                self.infos[u'房子类型'] = u'-1'  # 导出数据时，为了防止改成 number_format 错误，把字符串换成数值

            self.infos[u'小区名称'] = soup.select('.info')[0].text
            self.infos[u'区域'] = soup.select('.info > a')[0].text
            # infos[u'地区'] = soup.select('.info > a')[1].text
            self.infos[u'详细区域'] = soup.select('.info')[1].text
            self.infos[u'链家编号'] = soup.select('.info')[3].text
            self.infos[u'关注房源'] = soup.select('#favCount')[0].text + u"人关注"
            self.infos[u'看过房源'] = soup.select('#cartCount')[0].text + u"人看过"

            partent = re.compile('<li><span.*?class="label">(.*?)</span>(.*?)</li>')
            result = re.findall(partent, res.text)

            for item in result:
                if item[0] != u"抵押信息" and item[0] != u"房本备件":
                    self.infos[item[0]] = item[1]
                if item[0] == u'产权年限':
                    self.infos[u'产权年限'] = item[1]
            
            # 挂牌时间等信息，格式有变化，重新添加正则表达式
            partent = re.compile('<li>\s*<span.*?class=.*?>(.*?)</span>\s+<span>(.*?)</span>\s+</li>')
            result = re.findall(partent, res.text)

            for item in result:
                #print unicode(item[0]),unicode(item[1])
                if item[0] == u'挂牌时间':
                    self.infos[u'挂牌时间'] = item[1]
                if item[0] == u'交易权属':
                    self.infos[u'交易权属'] = item[1]
                if item[0] == u'上次交易':
                    self.infos[u'上次交易'] = item[1]
                if item[0] == u'房屋用途':
                    self.infos[u'房屋用途'] = item[1]
                if item[0] == u'房屋年限':
                    self.infos[u'房屋年限'] = item[1]
                if item[0] == u'产权所属':
                    self.infos[u'产权所属'] = item[1]
                if item[0] == u'房本备件':
                    self.infos[u'房本备件'] = item[1]    
            
            row = index + (self.page - 1) * 30
            self.infos[u'序号'] = str(row + 1)
            self.infos[u'状态'] = u'在售'
            self.infos[u'城市'] = self.cityConstant.cityToChinese[self.city]
            
            self.logger.log.info('taskId: ' + str(self.taskIndex) + ' row: ' + str(row) + ' / {0} {1}%'.format(self.totalCount,round(float(row)/self.totalCount * 100, 2)))
            if row == 0:
                for index_item in self.elementConstant.data_constant.keys():
                    self.generateExcel.writeExcelPositon(0, self.elementConstant.data_constant.get(index_item),
                                                          index_item)

                self.wirte_source_data(1)

            else:
                row = row + 1
                self.wirte_source_data(row)
        return self.infos

    # 封装统一 request 请求,采取动态代理和动态修改 User-Agent 方式进行访问设置,减少服务端手动暂停的问题
    def requestUrlForRe(self, url):
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
                return self.requestUrlForRe(url)
        except Exception as e:
            self.proxyServer = self.getIpProxy.get_random_ip()
            s = requests.session()
            s.keep_alive = False
            return self.requestUrlForRe(url)

    # 源数据生成,写入Excel中,从infos字典中读取数据,放置到list列表中进行写入操作,其中可修改规定写入格式
    def wirte_source_data(self, row):
        for itemKey in self.infos.keys():            
            item_valus = self.infos.get(itemKey)
            if itemKey == u'详细区域':
                temps_item_valus = item_valus.replace(u'\xa0',u' ').split(u' ')
                self.generateExcel.writeExcelPositon(row, self.elementConstant.data_constant.get(u'所属下辖区'),temps_item_valus[0])
                self.generateExcel.writeExcelPositon(row, self.elementConstant.data_constant.get(u'所属商圈'),temps_item_valus[1])
                self.generateExcel.writeExcelPositon(row, self.elementConstant.data_constant.get(u'所属环线'),temps_item_valus[2])
            else:
                tempItemKey = self.elementConstant.unit_check_name(itemKey)
                count = self.elementConstant.data_constant.get(tempItemKey)
                # print itemKey, unicode(tempItemKey), self.elementConstant.data_constant.get(tempItemKey), item_valus
                if tempItemKey != None and count != None:
                    # todo 检查使用标准,修改使用逻辑
                    if tempItemKey == u'链家编号':
                        item_valus = item_valus[0:len(item_valus) - 2]
                    elif tempItemKey == u'单价':
                        item_valus = item_valus[0:len(item_valus) - 4]
                    elif tempItemKey == u'建筑面积':
                        item_valus = item_valus[0:len(item_valus) - 1]
                    elif tempItemKey == u'建成时间':
                        if u'年' in item_valus:
                            item_valus = item_valus[0:item_valus.index(u'年')]
                        else:
                            # 有些城市没有建成时间，因为 beautiful soup 的关系，会解析为建筑类型。此时不要这个字段就好了
                            item_valus = str(-1)
                    elif tempItemKey == u'关注人数' or tempItemKey == u'看过房源':
                        item_valus = item_valus[0:len(item_valus) - 3]
                    elif tempItemKey == u'挂牌时间':
                        item_valus = item_valus.replace('-', '/')
                    elif tempItemKey == u'上次交易':
                        item_valus = item_valus.replace('-', '/')

                    self.generateExcel.writeExcelPositon(row,
                                                          self.elementConstant.data_constant.get(tempItemKey),
                                                          item_valus)

if "__name__" == "__main__":
    if len(sys.argv) >= 5:
        print(u'[Params] {0} {1} {2} {3} {4}'.format(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]))
        worker = spiderWorker()
        worker.prepare(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
        worker.start()
    else:
        print(u'[ERROR] 参数不足')
    
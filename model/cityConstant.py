# -*- coding: utf-8 -*-

class cityConstant:
    
    def __init__(self):
        self.cityToBref = {}
        self.cityToChinese = {}
        self.cityPriceIntervals = {}
        self.initData()

    def initData(self):
        # 城市缩写，用于拼接请求所用的 URL
        # 目前追踪：北京，上海，广州，深圳，杭州，苏州，西安
        self.cityToBref = {u'beijing' : u'bj',\
                         u'shanghai': u'sh',\
                         u'guangzhou': u'gz',\
                         u'shenzhen': u'sz',\
                         u'hangzhou': u'hz',\
                         u'suzhou': u'su',\
                         u'xian': u'xa',\
                         #u'chengdu': u'cd',\
                         #u'tianjin': u'tj',\
                         #u'zhengzhou': u'zz',\
                         }
        
        # 城市中文名称（填写如 xlsx 使用）
        self.cityToChinese = {u'beijing' : u'北京',\
                         u'shanghai': u'上海',\
                         u'guangzhou': u'广州',\
                         u'shenzhen': u'深圳',\
                         u'hangzhou': u'杭州',\
                         u'suzhou': u'苏州',\
                         u'xian': u'西安',\
                         #u'chengdu': u'cd',\
                         #u'tianjin': u'tj',\
                         #u'zhengzhou': u'zz',\
                         }
        
        # 城市价格区间（保证每个分页数据量少于 3000 条，即 100 页）
        self.cityPriceIntervals = {}
        self.cityPriceIntervals[u'beijing'] = [0,160,210,240,260,275,290,305,320,335,350,365,380,395,410,425,440,455,470,485,500,520,540,560,580,600,630,660,690,730,780,830,890,960,1080,1250,1500,2200,10000]
        self.cityPriceIntervals[u'shanghai'] = [0,145,175,195,210,225,240,255,270,285,300,315,330,345,365,385,410,435,470,510,550,610,680,760,850,950,1150,1400,2200,10000]
        self.cityPriceIntervals[u'guangzhou'] = [0,80,105,125,140,155,165,175,185,195,205,215,225,235,250,260,275,290,305,325,340,360,390,430,480,560,700,1400,10000]
        self.cityPriceIntervals[u'shenzhen'] = [0,166,200,233,266,300,320,340,366,400,430,460,500,533,566,600,633,700,800,900,1200,1500,3000,10000]
        self.cityPriceIntervals[u'hangzhou'] = [0,90,110,133,150,166,183,200,210,220,232,248,260,275,285,300,320,333,350,375,400,433,480,533,620,700,1000,10000]
        self.cityPriceIntervals[u'suzhou'] = [0,66,100,120,133,150,166,182,200,218,233,250,266,282,300,320,333,366,400,433,500,620,800,1000,10000]
        self.cityPriceIntervals[u'xian'] = [0,44,66,80,90,100,110,120,127,133,142,150,158,170,182,200,218,250,300,400,800,10000]
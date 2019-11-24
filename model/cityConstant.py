# -*- coding: utf-8 -*-


class cityConstant:

    def __init__(self):
        self.cityToBref = {}
        self.cityToChinese = {}
        self.cityPriceIntervals = {}
        self.initData()

    def initData(self):
        # 城市缩写，用于拼接请求所用的 URL
        # 目前追踪：北京，上海，广州，深圳，杭州，苏州，厦门（武汉，南京，天津）
        self.cityToBref = {u'beijing': u'bj',
                           u'shanghai': u'sh',
                           u'guangzhou': u'gz',
                           u'shenzhen': u'sz',
                           u'hangzhou': u'hz',
                           u'suzhou': u'su',
                           u'xiamen': u'xm',\
                           # u'wuhan': u'wh',\
                           # u'tianjin': u'tj',\
                           # u'nanjing': u'nj'\
                           }

        # 城市中文名称（填写如 xlsx 使用）
        self.cityToChinese = {u'beijing': u'北京',
                              u'shanghai': u'上海',
                              u'guangzhou': u'广州',
                              u'shenzhen': u'深圳',
                              u'hangzhou': u'杭州',
                              u'suzhou': u'苏州',
                              u'xiamen': u'厦门',\
                              # u'wuhan': u'武汉',\
                              # u'tianjin': u'天津',\
                              # u'nanjing': u'南京'\
                              }

# -*- coding: utf-8 -*-

# 修改默认抓取数据,进行数据优化

class elementConstant:
    def __init__(self):
        self.data_constant = {}
        self.init_source_data()
        index = 0

    def init_source_data(self):
        
        # 序号
        self.data_constant[u'序号'] = 0  
        # 链家编号
        self.data_constant[u'链家编号'] = 1
        # 状态（基本无用，手写的在售）
        self.data_constant[u'状态'] = 2
        # 每平方售价 单价（元/平米）
        self.data_constant[u'单价'] = 3
        # 建筑面积：平米
        self.data_constant[u'建筑面积'] = 4
        # 套内面积
        self.data_constant[u'套内面积'] = 5 
        # 房屋总价
        self.data_constant[u'总价'] = 6
        # 挂牌时间 挂牌时间
        self.data_constant[u'挂牌时间'] = 7
        # 上次交易 上次交易时间
        self.data_constant[u'上次交易'] = 8
        # 房子类型 建成时间：年 注释：房屋类型包含　　1990年建/塔楼　需要进行元组分割
        self.data_constant[u'建成时间'] = 9
        #
        self.data_constant[u'城市'] = 10  # 城市需要进行默认转化
        # 详细区域 '朝阳 垡头 四至五环'　以空格区分进行匹配
        # example ：所属下辖区  朝阳
        # 所属商圈　垡头
        # 所属环线　四至五环
        self.data_constant[u'所属下辖区'] = 11
        self.data_constant[u'所属商圈'] = 12
        # 小区名称　所属小区
        self.data_constant[u'所属小区'] = 13
        self.data_constant[u'所属环线'] = 14
        # 房屋户型 户型
        self.data_constant[u'户型'] = 15
        # 朝向 朝向
        self.data_constant[u'朝向'] = 16
        # 梯户比例 梯户比例
        self.data_constant[u'梯户比例'] = 17
        # 房屋用途 房屋用途 15
        self.data_constant[u'房屋用途'] = 18
        # 产权年限 产权年限
        self.data_constant[u'产权年限'] = 19
        # 建筑类型 建筑类型
        self.data_constant[u'建筑类型'] = 20
        # 交易权属 交易权属
        self.data_constant[u'交易权属'] = 21
        # 装修情况 装修情况
        self.data_constant[u'装修情况'] = 22
        # 建筑结构 建筑结构
        self.data_constant[u'建筑结构'] = 23
        # 供暖方式 供暖方式
        self.data_constant[u'供暖方式'] = 24
        # 产权所属 产权所属
        self.data_constant[u'产权所属'] = 25
        # 户型结构 户型结构 23
        self.data_constant[u'户型结构'] = 26
        # 配备电梯 配备电梯
        self.data_constant[u'配备电梯'] = 27
        # 所在楼层 楼层
        self.data_constant[u'楼层'] = 28
        # 房屋年限 房屋年限
        self.data_constant[u'房屋年限'] = 29
        # 标题 标题
        self.data_constant[u'标题'] = 30
        # 网址 网址
        self.data_constant[u'网址'] = 31
        # 关注房源 关注（人）
        self.data_constant[u'关注人数'] = 32
        # 看过房源 看过房源：人
        self.data_constant[u'看过房源人数'] = 33


    # 根据字段名称，返回写入 Excel 表中的列号
    def column_position(self, temp_data):
        return self.data_constant.get(temp_data)

    # 检测匹配是否包含
    def unit_check_name(self, temp_data):
        if temp_data in self.data_constant.keys():
            return temp_data
        else:
            if temp_data == u'每平方售价':
                return u'单价'
            if temp_data == u'建筑面积':
                return u'建筑面积'
            if temp_data == u'上次交易':
                return u'上次交易'
            if temp_data == u'房子类型':
                return u'建成时间'
            if temp_data == u'小区名称':
                return u'所属小区'
            if temp_data == u'户型':
                return u'户型'
            if temp_data == '所在楼层':
                return '楼层'
            if temp_data == u'关注房源':
                return u'关注人数'
            if temp_data == u'看过房源':
                return u'看过房源人数'

# Element_Constant = elementConstant()
# Element_Constant.excleTest()

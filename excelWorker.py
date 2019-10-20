# -*- coding: utf-8 -*-
import xlrd
import xlwt
import sys
import os

class excelWorker:
    # 初始化构造函数
    def __init__(self):
        # 多文件游标
        self.cursor = 0
        # 取出城市标签，如 beijing
        self.xlsPathIdentifier =  str(sys.argv[1])
        # 最终整表数据个数
        self.totalCount = 0
        # 获取 xls 文件集合
        self.xlsFiles = []
        path = os.path.join(os.getcwd(),self.xlsPathIdentifier)
        # 结果文件路径
        self.resultPath = os.path.join(os.getcwd(),self.xlsPathIdentifier,u'{0}全部数据.xls'.format(self.xlsPathIdentifier))
        # 先删除旧文件
        if os.path.exists(self.resultPath):
            os.remove(self.resultPath)
        
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '.xls' in name:
                    self.xlsFiles.append(os.path.join(root,name))
                    #data = xlrd.open_workbook(xlsFiles[0])
                    #table = data.sheets()[0]
                    #count = count + table.nrows
        
    # 整合多个 xls 文件到一张表
    def combine(self):
        if len(self.xlsFiles) <= 0:
            print(u'没有找到任何文件')
            exit()
        # 创建文件
        resultXLS = xlwt.Workbook()
        resultSheet = resultXLS.add_sheet(u'在售列表',cell_overwrite_ok=True)
        # 写入 sheet 头
        data = xlrd.open_workbook(self.xlsFiles[0])
        table = data.sheets()[0]
        title_row = table.row_values(0)
        for i in range(0,len(title_row)):
            resultSheet.write(0,i,title_row[i])
        self.cursor = 1
        
        # 批量写入
        for xlsFile in self.xlsFiles:
            data = xlrd.open_workbook(xlsFile)
            table = data.sheets()[0]
            nrows = table.nrows - 1 # 去掉标题
            ncols = table.ncols
            
            print(u'{0} 数据条目：{1}'.format(xlsFile,nrows))
            for row in range(1,nrows+1):
                for col in range(0,ncols):
                    row_values = table.row_values(row)
                    #ctype = 1 # 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    #if col in [0, 3, 4, 6, 9, 32]:
                    #    ctype = 2
                    #style = xlwt.XFStyle()
                    
                    # 如果是序号列，用新的覆盖
                    if col == 0:
                        resultSheet.write(self.cursor,col,self.cursor)
                    # 数字类型列号 0 3 4 6 9 32（注意，有些会转变失败，真正统计前，还是需要手动把列转成数字）
                    elif col in [3, 4, 6, 9, 32]:
                        value = row_values[col]
                        if value.isdigit():
                            value = round(float(row_values[col]),2)
                        else:
                            value = value
                        resultSheet.write(self.cursor,col,value)
                    else:
                        resultSheet.write(self.cursor,col,row_values[col])
                self.cursor = self.cursor + 1
                self.totalCount = self.totalCount + 1
        # 保存
        resultXLS.save(self.resultPath)
        print(u'整合最终数据条目 {0}'.format(self.totalCount))

worker = excelWorker()
worker.combine()
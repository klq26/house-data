# -*- coding: utf-8 -*-
import xlrd
import xlwt
import sys

class generateExcel:
    def __init__(self):
        self.raws = []
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.style = xlwt.XFStyle()

    def writeExcelPositon(self, rowNumber, column, source_data):
        self.ws.write(rowNumber, column, source_data)

    def wirte_Excel_In_style(self, rowNumber, column, source_data, style):
        self.ws.write(rowNumber, column, source_data, style)

    def saveExcel(self, name):
        # u'LianJiaSpider.xls'
        self.wb.save(name)

    def addSheetExcel(self, sheetName):
        self.ws = self.wb.add_sheet(sheetName,cell_overwrite_ok=True)
        # ##读文件占时未使用到
        # def readExcel(self):
        #     ExcelData = xlrd.open_workbook("example.xls")
        #     table = ExcelData.sheets()[0]
        #     # 获取整行数据
        #     tablerow = table.row_values(1)
        #     # 获取整列数据
        #     table_col = table.col_values(1)
        #     # 5、获取行数和列数　
        #     table.nrows
        #     table.ncols
        #     # 6、获取单元格
        #     table.cell(0, 0).value
        #     table.cell(0, 0).value
        #     print tablerow, table_col

# generateExcel = generateExcel()
#
# generateExcel.start()

# -*- sudDirsding: utf-8 -*-
import os
import sys
import json
import re
import time

from model.elementConstant import elementConstant


class checkUnFinishTask:
    # 初始化构造函数
    def __init__(self):
        self.unfinished = []
        subDirs = self.getSubDirs(os.path.join(os.getcwd(), u'output'))
        self.dateFolder = time.strftime("%Y%m", time.localtime())
        for dir in subDirs:
            if os.path.basename(dir) == u'unfinished':
                continue
            # print(dir)
            cityName = os.path.basename(dir)
            jsonPath = os.path.join(dir, u'{0}.json'.format(cityName))
            if os.path.exists(jsonPath):
                with open(jsonPath, u'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                    for item in data:
                        #logFile = os.path.join(dir, self.dateFolder, item[u'logFile'])
                        xlsxFile = os.path.join(
                            dir, self.dateFolder, item[u'xlsxFile'])
                        item['city'] = cityName
                        if not os.path.exists(xlsxFile):
                            print('{0} \ {1} 没完成'.format(
                                cityName, item[u'url']))
                            self.unfinished.append(item)
                with open(os.path.join(dir, u'{0}.json'.format(cityName)), u'w+', encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False,
                                       sort_keys=True, indent=4, separators=(',', ':')))
        # print(len(self.unfinished))
        # for d in self.unfinished:
        #     print(d)
        # 以 10 为间隔，输出多个未完成文件的 json 数据集
        totalCount = len(self.unfinished)
        interval = 10
        fileCount = 0
        if totalCount % interval > 0:
            fileCount = int(totalCount / interval) + 1
        else:
            fileCount = int(totalCount / interval)
        for i in range(1, fileCount+1):
            with open(os.path.join(os.getcwd(), u'output', u'unfinished', u'unfinished_{0}.json'.format(i)), u'w+', encoding='utf-8') as f:
                startIdx = (i - 1) * interval
                if startIdx + interval > totalCount:
                    endIdx = totalCount
                else:
                    endIdx = startIdx + interval
                # print(startIdx, endIdx)
                dicts = self.unfinished[startIdx: endIdx]
                # for d in dicts:
                #     print(d)
                f.write(json.dumps(dicts, ensure_ascii=False,
                                   sort_keys=True, indent=4, separators=(',', ':')))

    # 只获取一级目录
    def getSubDirs(self, rootPath):
        # 目录深度基准（父路径的 \ 级数）
        rootDepth = len(rootPath.split(os.path.sep))
        subDirs = []  # 存放第1级子目录
        for root, dirs, files in os.walk(rootPath, topdown=True):
            for dir in dirs:
                dirPath = os.path.join(root, dir)
                dirDepth = len(dirPath.split(os.path.sep))
                if dirDepth == rootDepth + 1:
                    subDirs.append(dirPath)
                else:
                    break
        return subDirs


if __name__ == "__main__":
    checker = checkUnFinishTask()

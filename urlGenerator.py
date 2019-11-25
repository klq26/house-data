import os
import sys
import re
import json
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from model.cityConstant import cityConstant


class urlGenerator:

    def __init__(self, city):
        self.city = city
        self.cityConstant = cityConstant()
        # 根据 beijing 生成 bj 本地字典
        self.cityBref = self.cityConstant.cityToBref[self.city]
        # 生成占位链接
        self.urlHolder = u'https://' + self.cityBref + \
            '.lianjia.com/ershoufang/pgbp{0}ep{1}/'
        self.logFileHolder = u'worker_begin{0}_end{1}.log'
        self.outputFileHolder = u'HouseData_begin{0}_end{1}.xlsx'

    # 把 0w ~ 10000w 的房屋信息近似分成 2000+ 一个区间，供后续 worker 抓取信息
    def intelligentDetect(self, interval=5, expectLow=2000, expectHigh=3000):
        # 上下限
        min = 0
        max = 10000
        # 初始化
        begin = min
        end = begin + interval
        totalCount = 0
        # 价格区间结果集
        durations = []
        # 是否因为超过 expectHigh 而退回
        isFallback = False

        """
        说明：以 min 为下限，每次增加 interval 万，从链家取数据并解析 totalCount
        1）如果 totalCount 小于 expectLow 最小 worker 期待数，则继续把上边界调高 interval 万
        2）如果 totalCount 大于 expectLow 并小于 expectHigh，这是我们最期望的结果，产出一条价格区间，存入 durations
        3）如果 totalCount 大于 expectHigh，则需要回滚最后一次增加的 interval，然后仅仅增加 interval 的 1/5，项目中最小的 interval 是 5w，回滚后，会 1w 1w 的增加
        4）如果触发回滚，isFallback 标识位会变成 True，此时因为上一次超过了 expectHigh 即 3000，所以就算回滚后，不足 expectLow 即 2000，也应该产出一条价格区间，否则程序陷入死循环
        5）因为房价超过 1500w 的房子在中国是少数，所以当上边界达到 1500w 时，interval 变成 100。当上边界达到 2500w 时，interval 变成 500。这是为了提高执行效率
        5）最后，把所有的价格区间，输出到文件
        """

        # 当总数不到 expectLow 即 2000 且上边界没超过 10000 时，继续执行
        while totalCount < expectLow and end <= max + 200:
            # 房屋价格超过 1500w 和 2500w 时，提高 interval，加快执行速度
            if end >= 1500:
                interval = 100
            if end >= 2500:
                interval = 500
            url = self.urlHolder.format(begin, end)
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url.replace('pg', 'pg1'), verify=False)
            #print(u'检查 URL：{0}'.format(url))
            partent = re.compile(
                '<h2 class="total fl">.*?<span>\s*(.*?)\s</span>.*?</h2>')
            result = re.findall(partent, response.text)
            if len(result) > 0:
                totalCount = int(result[0])
                print(u'{0}\t{1}'.format(url, totalCount))

            if totalCount < expectLow:
                if isFallback:
                    # 如果按最小间隔回退，直接到了少于 expectLow 的数量，也只好接受
                    if totalCount % 30 > 0:
                        pageCount = int(totalCount / 30) + 1
                    else:
                        pageCount = int(totalCount / 30)
                    print(u'\n★ 价格区间：{0}\t{1}\t{2}\n'.format(
                        url, totalCount, pageCount))
                    logFile = self.logFileHolder.format(begin, end)
                    xlsxFile = self.outputFileHolder.format(begin, end)
                    durations.append({u'url': url, u'totalCount': totalCount, u'pageCount': pageCount,
                                      u'logFile': logFile, u'xlsxFile': xlsxFile, u'city': self.city})
                    begin = end
                    end = end + interval
                    totalCount = 0
                    isFallback = False
                else:
                    # 数据量过少，继续增加上边界
                    end = end + interval
            elif totalCount >= expectLow and totalCount <= expectHigh:
                # 最佳结果
                if totalCount % 30 > 0:
                    pageCount = int(totalCount / 30) + 1
                else:
                    pageCount = int(totalCount / 30)
                print(u'\n★ 价格区间：{0}\t{1}\t{2}\n'.format(
                    url, totalCount, pageCount))
                logFile = self.logFileHolder.format(begin, end)
                xlsxFile = self.outputFileHolder.format(begin, end)
                durations.append({u'url': url, u'totalCount': totalCount, u'pageCount': pageCount,
                                  u'logFile': logFile, u'xlsxFile': xlsxFile, u'city': self.city})
                begin = end
                end = end + interval
                totalCount = 0
                isFallback = False
            elif totalCount > expectHigh:
                # 超出 expectHigh 即 3000 了，回退一个单位（如 1w），直至 totalCount 数据回到 (2000,3000) 之间，或直接小于 expectLow，都可以接受
                print('超出范围，end 退回：{0}w'.format(int(end - interval/5)))
                end = int(end - interval/5)
                totalCount = 0
                isFallback = True

            # 如果达到 10000w 了，直接生成最后一条数据，程序结束
            if end >= max:
                if totalCount % 30 > 0:
                    pageCount = int(totalCount / 30) + 1
                else:
                    pageCount = int(totalCount / 30)
                print(u'\n★ 价格区间：{0}\t{1}\t{2}\n'.format(
                    url, totalCount, pageCount))
                logFile = self.logFileHolder.format(begin, end)
                xlsxFile = self.outputFileHolder.format(begin, end)
                durations.append({u'url': url, u'totalCount': totalCount, u'pageCount': pageCount,
                                  u'logFile': logFile, u'xlsxFile': xlsxFile, u'city': self.city})
                begin = end
                end = end + interval
                totalCount = expectHigh + 1
                isFallback = False

            # 别太频繁，防止链家屏蔽
            time.sleep(0.5)
        filepath = os.path.join(os.getcwd(), u'output',
                                self.city, '{0}.json'.format(self.city))
        with open(filepath, 'w+', encoding='utf-8') as jsonFile:
            jsonFile.write(json.dumps(durations, ensure_ascii=False,
                                      sort_keys=True, indent=4, separators=(',', ':')))


if __name__ == '__main__':
    # 根据 beijing 生成 bj 本地字典
    if len(sys.argv) <= 1:
        print(u'[ERROR] 参数不足，需要城市的拼音，如 beijing')
        exit()
    detector = urlGenerator(str(sys.argv[1]))
    detector.intelligentDetect(5, 2000, 3000)

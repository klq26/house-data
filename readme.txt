说明

1. 调用 python sailingInfoSpider.py beijing 可以查询 beijing 目录下 url.txt 中的所有筛选列表页数据。
2. 实际查找前，建议先调用 python testUrlCount.txt 看看之前的筛选条件是否溢出，即筛选结果大于 3000 条，页数大于 100，如此则需要重新调整 url.txt 保证每条 url 下的筛选列表结果数少于 3000 条
3. 如果发生 worker.py 卡死的情况，可以在该窗口上，复制出调度器 sailingInfoSpider.py 传递过来的参数，以确定具体是哪个 worker 卡死，再手动重新执行 worker 即可，如“python worker.py https://xxx 3 huairou beijing”
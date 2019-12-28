说明

1. 调用 python sailingInfoSpider.py beijing 可以查询 output\beijing 目录下 beijing.json 中的所有筛选列表页数据。
2. beijing.json 是由 python urlGenerator.py beijing 生成，是自动嗅探模式。
3. 如果发生 worker.py 卡死的情况，后续可以通过 checkUnFinishTask.py 检查有哪些任务没有拿到 xlsx 数据，然后生成 unfinished_x.json(x = 1 2 3 4)
4. 之后用 python sailingInfoSpider.py unfinished_1 这样的命令，逐一执行残留任务。json 文件指明了保存 xlsx 文件的路径，不会出错。

5. 尝试在 worker.py 中增加 time.sleep(x) 降低查询频率，防止被服务器拒绝。（目前看无此需要）
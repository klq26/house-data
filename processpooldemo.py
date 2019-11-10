import multiprocessing
import time
import os
import random
import traceback

def work(msg, queue):

    try:
        isSuccess = bool(random.getrandbits(1))
        t_start = time.time()   
        print("索引号：%s 进程号：%d work 开始执行\n" % (msg, os.getpid()))
        # 故意搞个崩溃
        if not isSuccess:
            print("%{0}" %(msg, msg))
        for i in range(1,2):
            time.sleep(1)
            print("索引号：%s 进程号：%d work 进程执行中... 进度：%d\n" % (msg, os.getpid(),i))
        t_stop = time.time()
    except Exception as e:
        queue.put(u'★ pid {0} taskid {1} status:{2} traceback msg:\n{3}'.format(os.getpid(), msg, isSuccess,traceback.format_exc()))
        #print(u'Exception: {0}'.format(repr(e)))    # 给出较全的异常信息，包括异常信息的类型，如1/0的异常信息
    else:
        print("索引号：%s 进程号：%d work 进程执行完毕。耗时 %.2f\n" % (msg, os.getpid(), t_stop - t_start))
        queue.put(u'pid {0} taskid {1} status {2}'.format(os.getpid(), msg, isSuccess))

def report(msg, queue):
    print("report 进程启动：(%s)，父进程为：(%s)\n\n\n" % (os.getpid(), os.getppid()))
    #print(queue.qsize())
    for i in range(queue.qsize()):
        print("各进程执行状态：%s" % queue.get(True))

if __name__ == "__main__":
    # 进程池，同时最大运行 3 个进程
    po = multiprocessing.Pool(3)
    # 队列，收集每个进程的返回值
    queue = multiprocessing.Manager().Queue()
    # 模拟总共 10 个任务
    for i in range(1, 11):
        # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
        # 每次循环将会用空闲出来的子进程去调用目标
        po.apply_async(work, (i, queue))
    print("-----start-----")
    po.close() # 关闭进程池，关闭后po不再接收新的请求
    po.join() # 等待po中所有子进程执行完成，必须放在close语句之后
    # 报告所有进程的执行结果
    report('report', queue)
    print("-----end-----")
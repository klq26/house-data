import multiprocessing
import time
import os
import random

def test2(msg):
    t_start = time.time()   
    print("%s开始执行，进程号为%d" % (msg, os.getpid()))
    time.sleep(random.random() * 2)  
    t_stop = time.time()
    print("%s执行完成，耗时%.2f" % (msg, t_stop - t_start)) 
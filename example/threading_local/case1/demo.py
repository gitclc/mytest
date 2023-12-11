"""
当我们运行多个线程时，可能会需要在每个线程中保留线程中独立的一个变量，例如uuid
我们经常会想要在线程之外定义这个变量，但是多线程的情况下并不能保证这个变量的线程安全性
例如当前样例中 th_local 会被其他线程给修改掉

为了让变量变得安全，很多人可能会想到使用线程的id，以key和value的形式来保存变量，
但是什么时候回收这些变量就会成为问题

实际上python官方有提供线程独立变量的使用方法，在case2中对该方法进行了简单应用
"""
import random
import threading
import time
import uuid

th_local = type('th_local', tuple(), {'id': None})


def sub_func():
    global th_local
    cur_id = threading.get_ident()
    print('子函数:[线程id:{},guid:{}]'.format(cur_id, th_local.id))


def th_local_test():
    global th_local
    cur_id = threading.get_ident()
    guid = uuid.uuid4()
    print('线程{}开始执行,当前guid:{}'.format(cur_id, guid))
    th_local.id = guid
    time.sleep(random.random() * 5)
    print('主函数:[线程id:{},guid:{}]'.format(cur_id, th_local.id))
    sub_func()


if __name__ == '__main__':
    for i in range(5):
        a = threading.Thread(target=th_local_test)
        a.start()

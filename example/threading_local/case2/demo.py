"""
threading.local 代码示例
"""
import random
import threading
import time
import uuid

th_local = threading.local()


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

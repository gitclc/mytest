import datetime
import time


def countdown(sec: int):
    """
    倒计时计时器
    """
    start_time = time.time()  # 倒计时开始时间

    def reset_time():
        """
        重置倒计时开始时间
        """
        nonlocal start_time
        start_time = time.time()

    def inner():
        # 判断倒计时是否结束:
        # 1.计时结束则重置开始时间，返回True
        # 2.计时未结束返回False
        if time.time() - start_time > sec:
            reset_time()
            return True
        else:
            print('\r倒计时还剩{}秒'.format(round(sec - time.time() + start_time, 0)), end='')
            return False

    inner.reset_time = reset_time  # reset_time方法提供给外部调用
    return inner


if __name__ == '__main__':
    a = countdown(10)  # 创建时倒计时即开始
    time.sleep(2)
    a.reset_time()  # 重置倒计时开始时间
    while not a():
        time.sleep(0.1)

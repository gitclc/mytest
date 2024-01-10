print(__name__, '开始加载')


# print('test B module')


def test():
    print('call B.test func')


def B():
    print('this is B function')
    test()


print(__name__, '加载结束')

# 源码出处：from functools import lru_cache
from collections import namedtuple
from _thread import RLock


class _HashedSeq(list):
    """ This class guarantees that hash() will be called no more than once
        per element.  This is important because the lru_cache() will hash
        the key multiple times on a cache miss.
    """

    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)  # 对tup做hash操作，这意味着tup的每个元素都必须是可hash的

    # 定义hash 方法，使该类可以作为字典的key使用
    def __hash__(self):
        # 直接返回已hash的值，避免取dict的key时反复进行hash操作
        return self.hashvalue


def _make_key(args, kwds, typed,
              kwd_mark=(object(),),
              fasttypes={int, str},
              tuple=tuple, type=type, len=len):
    # All of code below relies on kwds preserving the order input by the user.
    # Formerly, we sorted() the kwds before looping.  The new way is *much*
    # faster; however, it means that f(x=1, y=2) will now be treated as a
    # distinct call from f(y=2, x=1) which will be cached separately.
    key = args  # 声明位置参数为key
    if kwds:  # 判断关键字参数是否为真
        key += kwd_mark  # key添加一个kwd_mark元素
        for item in kwds.items():  # 循环关键字参数的item
            key += item  # 在key后面添加item元素
    if typed:  # 判断typed 是否为真
        key += tuple(type(v) for v in args)  # 循环位置参数，并在key后面添加位置参数的类型
        if kwds:  # 判断关键字参数是否为真
            key += tuple(type(v) for v in kwds.values())  # 循环关键字参数的value，并在key后面添加位置参数的类型
    elif len(key) == 1 and type(key[0]) in fasttypes:  # 判断key的长度是否为1，如果为1的话,判断类型是否为整数和字符串
        return key[0]  # 返回key的第一个元素
    return _HashedSeq(key)  # 返回_HashedSeq类


WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)


def update_wrapper(wrapper,
                   wrapped,
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    for attr in assigned:  # 循环需要更新的字段
        try:
            value = getattr(wrapped, attr)  # 获取被装饰的函数需要更新的属性
        except AttributeError:
            pass  # 获取不到则跳过
        else:  # try ... else ... 如果执行不报错则执行else代码
            setattr(wrapper, attr, value)  # 更新装饰器的属性
    for attr in updated:  # 更新__dict__
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))  # 将被装饰的函数的__dict__ 更新到 装饰器的__dict__中
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped  # 将被装饰的函数保存在装饰器的__wrapped__ 属性中
    return wrapper  # 返回装饰器


def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    sentinel = object()  # 创建一个对象，获取不到缓存结果时作为默认值，用于判断是否结果是否已缓存
    make_key = _make_key  # 引用一个_make_key 函数，函数用于根据传入的参数创建一个可hash的对象
    PREV, NEXT, KEY, RESULT = 0, 1, 2, 3  # 定义一系列常量，用于实现循环链表，分别表示前一个节点、后一个节点、key、result

    cache = {}  # 定义一个字典，缓存函数执行结果
    hits = misses = 0  # 定义计数器初始值，hits表示命中次数，misses 表示未命中次数
    full = False  # 定义布尔值，缓存数据是否已满的标志位
    cache_get = cache.get  # 引用cache的get方法，方便调用
    cache_len = cache.__len__  # 引用cache的len方法，方便调用
    lock = RLock()  # 创建一个线程锁对象，保证修改cache时线程安全
    root = []  # 定义一个列表，用于记录循环链表元素
    root[:] = [root, root, None, None]  # 初始化循环链表，前一个节点和后一个节点都为自身

    # 外部函数已对maxsize处理，maxsize的值为（None , 0 , 大于0的整数）
    # 当maxsize 等于0 时，不作缓存
    if maxsize == 0:

        def wrapper(*args, **kwds):
            nonlocal misses  # 获取局部变量
            misses += 1  # 未命中次数加1
            result = user_function(*args, **kwds)  # 直接调用函数，获取结果
            return result  # 返回结果

    # 当maxsize 为None时，不限制缓存数量
    elif maxsize is None:

        def wrapper(*args, **kwds):
            nonlocal hits, misses  # 获取局部变量
            key = make_key(args, kwds, typed)  # 调用make_key,传入 位置参数，关键字参数，typed
            result = cache_get(key, sentinel)  # 获取cache中的数据，默认值为object()
            if result is not sentinel:  # 判断结果是否不为默认值
                hits += 1  # 不为默认值的话，命中加1
                return result  # 返回结果
            misses += 1  # 未命中次数加1
            result = user_function(*args, **kwds)  # 调用函数
            cache[key] = result  # 存储结果
            return result  # 返回结果
    # 当maxsize 为大于0的整数时
    else:

        def wrapper(*args, **kwds):
            # Size limited caching that tracks accesses by recency
            nonlocal root, hits, misses, full  # 获取局部变量
            key = make_key(args, kwds, typed)  # 获取key
            with lock:  # 获取线程锁
                link = cache_get(key)
                if link is not None:
                    # Move the link to the front of the circular queue
                    link_prev, link_next, _key, result = link  # 获取的link的（上一节点，下一个节点，key，result）
                    link_prev[NEXT] = link_next  # link的上一个节点指向link的下一个节点
                    link_next[PREV] = link_prev  # link的下一个节点指向link的上一个节点
                    last = root[PREV]  # 获取最后一个节点
                    last[NEXT] = root[PREV] = link  # 将当前的link放至最后
                    link[PREV] = last  # link的上一个节点指向last
                    link[NEXT] = root  # link的下一个节点指向root
                    hits += 1  # 命中次数加1
                    return result  # 返回结果
                misses += 1  # 未命中次数加1
            result = user_function(*args, **kwds)  # 执行函数
            with lock:  # 获取线程锁
                if key in cache:  # 判断key是否在缓存中
                    # 会执行到这里，说明在锁被释放的时候，有一个相同的key已经被缓存了
                    # 此处直接返回结果和更新未命中次数即可
                    # Getting here means that this same key was added to the
                    # cache while the lock was released.  Since the link
                    # update is already done, we need only return the
                    # computed result and update the count of misses.
                    pass
                elif full:  # 判断缓存是否已满
                    oldroot = root  # 声明root 为oldroot
                    oldroot[KEY] = key  # 记录key
                    oldroot[RESULT] = result  # 记录result

                    root = oldroot[NEXT]  # 声明root的下一个节点为root
                    oldkey = root[KEY]  # 获取key
                    oldresult = root[RESULT]  # 获取result
                    root[KEY] = root[RESULT] = None  # 设置root的key和result为None

                    del cache[oldkey]  # 删除root的缓存
                    cache[key] = oldroot  # 存储oldroot
                else:  # 未命中且缓存未满
                    # Put result in a new link at the front of the queue.
                    last = root[PREV]  # 获取root的前一个节点，即最后一个节点
                    link = [last, root, key, result]  # 创建一个新节点，新节点的上一个节点为最后一个节点，下一个节点为根节点
                    last[NEXT] = root[PREV] = cache[key] = link  # 新节点链接到上一个节点的后面，根节点的前面
                    full = (cache_len() >= maxsize)  # 记录节点是否已经满了
            return result

    def cache_info():
        """Report cache statistics"""
        with lock:  # 获取线程锁
            return _CacheInfo(hits, misses, maxsize, cache_len())  # 返回 命中次数，未命中次数，最大缓存数，缓存长度

    def cache_clear():
        """Clear the cache and cache statistics"""
        nonlocal hits, misses, full  # 获取局部变量
        with lock:  # 获取线程锁
            cache.clear()  # 清空缓存
            root[:] = [root, root, None, None]  # 清空循环链表
            hits = misses = 0  # 清空命中次数计数器
            full = False  # 清空缓存状态标志位

    wrapper.cache_info = cache_info  # 设置装饰器可调用方法
    wrapper.cache_clear = cache_clear  # 设置装饰器可调用方法
    return wrapper


_CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])


def lru_cache(maxsize=128, typed=False):
    """
    maxsize 的取值为 1.整数  2.None 3.可调用函数(即被装饰的函数)
    1.为None时，不对缓存的数量进行限制
    2.为 0 时，不作缓存，直接返回结果
    3.为大于0的整数时，缓存数量为maxsize
    4.为可调用函数时, 声明maxsize 为user_function,修改maxsize 为128

    typed 表示缓存key时，是否要使用参数的类型进行hash
    """
    # 判断maxsize
    if isinstance(maxsize, int):
        if maxsize < 0:
            maxsize = 0
    elif callable(maxsize) and isinstance(typed, bool):
        user_function, maxsize = maxsize, 128  # 重新设置参数
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)  # 获取真正的装饰器
        wrapper.cache_parameters = lambda: {'maxsize': maxsize, 'typed': typed}  # 设置装饰器可调用方法
        return update_wrapper(wrapper, user_function)  # 更新装饰器信息并返回
    elif maxsize is not None:
        raise TypeError(
            'Expected first argument to be an integer, a callable, or None')

    def decorating_function(user_function):
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)  # 获取真正的装饰器
        wrapper.cache_parameters = lambda: {'maxsize': maxsize, 'typed': typed}  # 设置装饰器可调用方法
        return update_wrapper(wrapper, user_function)  # 更新装饰器信息并返回

    return decorating_function


import random

"""
使用注意事项:
1.被装饰的函数参数必须可hash
2.如果结果会参与随机则不能缓存
3.关键字参数如果传入顺序不对，则会缓存多次。（例如：func(a=1,b=1)func(b=1,a=1)，会缓存两次）
4.typed参数为True时，会连同参数类型一起参与hash;
typed为False时，参数如(a=1,b=1.0)(a=1,b=1)(a=1.0,b=1.0)这三个参数只会被缓存一次;
而typed为True时，以上三个参数会被缓存三次
"""


@lru_cache(maxsize=0)
def test(a, b):
    print('test', 2)
    return random.random()


if __name__ == '__main__':
    pass
    # print(test(1, 2))
    # print(test(1.0, 2))
    # print(test(1, 2))
    # print(test.cache_info())  # 查看缓存信息
    # print(test.cache_clear())   # 清空缓存
    # print(test.cache_parameters())   # 查看装饰器输入参数
    # print(test.__wrapped__)  # 获取未被装饰的原函数

# from threading import local
from weakref import ref
from contextlib import contextmanager
from threading import current_thread, RLock, Thread


# 上下文管理器装饰器
# with 语法会执行到yield代码后停止，并创建一个作用域，当作用域结束时，会执行yield之后的代码
@contextmanager
def _patch(self):
    impl = object.__getattribute__(self, '_local__impl')  # 获取local的实现类
    try:
        dct = impl.get_dict()  # 调用get_dict方法
    except KeyError:  # 如果dict还未创建，则进入异常捕获
        dct = impl.create_dict()  # 为当前线程创建字典
        args, kw = impl.localargs  # 获取实现类的参数
        self.__init__(*args, **kw)  # 调用local的初始化方法
    with impl.locallock:  # 打开锁
        object.__setattr__(self, '__dict__', dct)  # 设置获取到的dct为local的__dict__属性
        yield


class _localimpl:
    """A class managing thread-local dicts"""
    __slots__ = 'key', 'dicts', 'localargs', 'locallock', '__weakref__'

    def __init__(self):
        # The key used in the Thread objects' attribute dicts.
        # We keep it a string for speed but make it unlikely to clash with
        # a "real" attribute.
        self.key = '_threading_local._localimpl.' + str(id(self))  # 创建一个唯一标识
        # { id(Thread) -> (ref(Thread), thread-local dict) }
        self.dicts = {}  # 创建一个字典

    def get_dict(self):
        """Return the dict for the current thread. Raises KeyError if none
        defined."""
        thread = current_thread()  # 获取当前线程
        return self.dicts[id(thread)][1]  # 根据当前线程id获取属于当前线程的字典

    def create_dict(self):
        """Create a new dict for the current thread, and return it."""
        localdict = {}  # 创建一个字典
        key = self.key  # 获取唯一标识
        thread = current_thread()  # 获取当前线程
        idt = id(thread)  # 获取当前线程id

        def local_deleted(_, key=key):
            # When the localimpl is deleted, remove the thread attribute.
            thread = wrthread()  # 获取当前线程
            if thread is not None:  # 判断线程是否存在
                del thread.__dict__[key]  # 删除线程中的当前实现类

        def thread_deleted(_, idt=idt):
            # When the thread is deleted, remove the local dict.
            # Note that this is suboptimal if the thread object gets
            # caught in a reference loop. We would like to be called
            # as soon as the OS-level thread ends instead.
            local = wrlocal()  # 获取实现类的弱引用对象
            if local is not None:  # 判断local是否已被回收
                dct = local.dicts.pop(idt)  # 从local的dicts属性中删除对应线程保存的数据

        # ref表示弱引用，ref的参数为 (弱引用对象，弱引用对象销毁时的回调函数)，当弱引用对象被回收时，返回None
        wrlocal = ref(self, local_deleted)  # 弱引用实现类，绑定回调函数
        wrthread = ref(thread, thread_deleted)  # 弱引用当前线程，绑定回调函数
        thread.__dict__[key] = wrlocal  # 在当前线程中添加属性，值为当前类的弱引用
        self.dicts[idt] = wrthread, localdict  # 当前类的字典存储 当前线程的弱引用，空字典
        return localdict  # 返回创建的字典


class local:
    __slots__ = '_local__impl', '__dict__'

    def __new__(cls, *args, **kw):
        if (args or kw) and (cls.__init__ is object.__init__):  # 判断是否传入参数以及__init__方法是否被重写
            raise TypeError("Initialization arguments are not supported")
        self = object.__new__(cls)  # 使用object创建一个实例
        impl = _localimpl()  # 创建一个_localimpl 实现类
        impl.localargs = (args, kw)
        impl.locallock = RLock()  # 创建线程锁
        object.__setattr__(self, '_local__impl', impl)  # 给实例设置一个_local__impl属性
        # We need to create the thread dict in anticipation of
        # __init__ being called, to make sure we don't call it
        # again ourselves.
        # 调用creat_dict,将当前类的弱引用添加到主线程的属性中，
        # 同时将主线程的引用和创建的字典添加到当前类的dicts属性中
        impl.create_dict()
        return self

    def __getattribute__(self, name):
        with _patch(self):
            return object.__getattribute__(self, name)  # 获取name对应的属性

    def __setattr__(self, name, value):
        # 判断要修改的属性是否为__dict__，如果是__dict__，提示__dict__为只读属性
        if name == '__dict__':
            raise AttributeError(
                "%r object attribute '__dict__' is read-only"
                % self.__class__.__name__)
        with _patch(self):
            return object.__setattr__(self, name, value)  # 设置属性

    def __delattr__(self, name):
        if name == '__dict__':
            raise AttributeError(
                "%r object attribute '__dict__' is read-only"
                % self.__class__.__name__)
        with _patch(self):
            return object.__delattr__(self, name)  # 删除属性


a = local()


def test(x):
    a.guid = x
    print(a._local__impl.dicts)
    print(a.__dict__)


if __name__ == '__main__':
    Thread(target=test, args=(5,)).start()
    test(3)

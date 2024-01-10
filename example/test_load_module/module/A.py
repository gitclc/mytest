print(__name__, '开始加载')
print(f'开始加载{__name__}子模块')

from example.test_load_module.module.B import B
from example.test_load_module.module.C import TB

print(f'{__name__}子模块加载结束')


def A():
    print('this is A function')
    B()
    a = TB()
    a.echo()


print(__name__, '加载结束')

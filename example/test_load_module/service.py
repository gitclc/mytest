import sys
import importlib
from abc import ABC

from tornado import web, gen
from tornado import ioloop

module_dict = {}


def load_moduel():
    global module_dict
    module_dict['A'] = importlib.import_module('example.test_load_module.module.A')
    module_dict['B'] = importlib.import_module('example.test_load_module.module.B')


def del_module_for_sys(module):
    print('删除模块:', module.__name__)
    del sys.modules[module.__name__]
    return module.__name__


class MainHandle(web.RequestHandler, ABC):

    @gen.coroutine
    def get(self, module):
        global module_dict
        print('=' * 30)
        # print(list(k for k, v in sys.modules.items() if v in module_dict.values()))
        if module == 'load':
            if module_dict:
                list(map(del_module_for_sys, list(module_dict.values())))
            #     module_dict['A'] = importlib.import_module('example.test_load_module.module.A')
            #     module_dict['B'] = importlib.import_module('example.test_load_module.module.B')
            #
            #     # module_dict['A'] = importlib.reload(module_dict['A'])
            #     # module_dict['B'] = importlib.reload(module_dict['B'])
            # else:
            module_dict['A'] = importlib.import_module('example.test_load_module.module.A')
            module_dict['B'] = importlib.import_module('example.test_load_module.module.B')
        elif module == 'call':
            arg = {k: v[0].decode() for k, v in self.request.arguments.items()}
            index = arg.get('index', None)
            print(arg)
            if index:
                getattr(module_dict[index], index)()
        self.write('load module')


def main():
    load_moduel()
    app = web.Application([
        ('/([^/]*)', MainHandle)
    ])
    app.listen(5830)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

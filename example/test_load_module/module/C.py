class Meta(type):
    def __new__(cls, *args, **kwargs):
        print('create model %s' % args[0])
        return type.__new__(cls, *args, **kwargs)


class Model(metaclass=Meta):
    def echo(self):
        print(self.__class__.__name__)


class TB(Model):
    a = 1
    pass


if __name__ == '__main__':
    a = TB()
    a.echo()

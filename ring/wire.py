import functools


class Wire(object):

    def __init__(self, preargs, anon_padding=False):
        assert isinstance(preargs, tuple)
        self.preargs = preargs
        self.anon_padding = anon_padding
        self.dynamic_attrs = {}

    def reargs(self, args, padding):
        if self.preargs:
            args = self.preargs + args
        elif padding and self.anon_padding:
            args = (None,) + args
        return args

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            pass

        attr = self.dynamic_attrs.get(name)
        if callable(attr):
            if callable(attr):
                @functools.wraps(self._body)
                def impl_f(*args, **kwargs):
                    args = self.reargs(args, padding=True)
                    return attr(args, kwargs)
                setattr(self, name, impl_f)

        return self.__getattribute__(name)
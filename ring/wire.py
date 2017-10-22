import functools


class WiredProperty(property):

    pass


class Wire(object):

    def reargs(self, args, preargs, padding):
        if preargs:
            args = preargs + args
        elif padding and self._shared_attrs.get('anon_padding', False):
            args = (None,) + args
        return args

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            pass

        attr = self._dynamic_attrs.get(name)
        if callable(attr):
            def impl_f(*args, **kwargs):
                args = self.reargs(args, padding=True)
                return attr(*args, **kwargs)
            setattr(self, name, impl_f)

        return self.__getattribute__(name)
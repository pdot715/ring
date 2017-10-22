import functools


class WiredProperty(property):

    pass


class Wire(object):

    @classmethod
    def for_callable(cls, f):
        from ring.func_base import is_method, is_classmethod

        _dynamic_attrs = {}

        if is_method(f):

            @WiredProperty
            def _w(self):
                wrapper_name = '__wrapper_' + f.__name__
                wrapper = getattr(self, wrapper_name, None)
                if wrapper is None:
                    _wrapper = cls((self,))
                    wrapper = functools.wraps(f)(_wrapper)
                    setattr(self, wrapper_name, wrapper)
                    _wrapper._dynamic_attrs = _dynamic_attrs
                return wrapper

        elif is_classmethod(f):
            _w = cls((), anon_padding=True)
        else:
            _w = cls(())

        _w._dynamic_attrs = _dynamic_attrs

        return _w

    def __init__(self, preargs, anon_padding=False):
        assert isinstance(preargs, tuple)
        self.preargs = preargs
        self.anon_padding = anon_padding

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

        attr = self._dynamic_attrs.get(name)
        if callable(attr):
            def impl_f(*args, **kwargs):
                args = self.reargs(args, padding=True)
                return attr(*args, **kwargs)
            setattr(self, name, impl_f)

        return self.__getattribute__(name)
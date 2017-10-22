
from ring.wire import Wire

import pytest


def test_wire_basic():

    @Wire.for_callable
    def f():
        return 42

    wire = f

    with pytest.raises(AttributeError):
        assert not wire.get_value()
    wire._dynamic_attrs['get_value'] = lambda: 10
    assert wire.get_value() == 10

    wire._dynamic_attrs['function'] = lambda a, b, c: a * 100 + b * 10 + c
    assert wire.function(3, 8, 6) == 386


def test_wire_class():

    class A(object):

        @Wire.for_callable
        def f(self):
            return 10

    wire = A.f
    wire._dynamic_attrs['sub'] = lambda self, a, b: a * 10 + b

    a = A()
    assert a.f.sub(7, 8) == 78


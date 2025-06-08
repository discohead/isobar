import pytest
import isobar as iso


def test_punaryfunction_square():
    f = lambda x: x * x
    a = iso.PUnaryFunction(f, start=0.0, stop=1.0, steps=5)
    assert a.nextn(5) == [0.0, 0.0625, 0.25, 0.5625, 1.0]
    with pytest.raises(StopIteration):
        next(a)


def test_punaryfunction_mul_offset():
    f = lambda x: x * x
    a = iso.PUnaryFunction(f, start=0.0, stop=1.0, steps=3, mul=2.0, offset=1.0)
    assert a.nextn(3) == [1.0, 1.5, 3.0]


def test_punaryfunction_rate_phase():
    f = lambda x: x * x
    a = iso.PUnaryFunction(
        f, start=0.0, stop=1.0, steps=3, rate=2.0, phase=0.5
    )
    assert a.nextn(3) == [0.25, 2.25, 6.25]


def test_pcallableunaryfunction_constant():
    f = lambda x: x * x
    c = iso.PCallableUnaryFunction(
        f,
        start=lambda t: 0.0,
        stop=lambda t: 1.0,
        steps=5,
        rate=lambda t: 1.0,
        phase=lambda t: 0.0,
        mul=lambda t: 1.0,
        offset=lambda t: 0.0,
    )
    assert c.nextn(5) == [0.0, 0.0625, 0.25, 0.5625, 1.0]


def test_pcallableunaryfunction_dynamic():
    f = lambda x: x * x
    d = iso.PCallableUnaryFunction(
        f,
        start=lambda t: 0.0,
        stop=lambda t: 1.0,
        steps=3,
        rate=lambda t: 1.0,
        phase=lambda t: 0.0,
        mul=lambda t: 2.0,
        offset=lambda t: t,
    )
    assert d.nextn(3) == [0.0, 1.0, 3.0]


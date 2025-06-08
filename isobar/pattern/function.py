from __future__ import annotations
from .core import Pattern
from typing import Callable

class PUnaryFunction(Pattern):
    """PUnaryFunction: Sample a unary function across a range.

    Args:
        function: Callable[[float], float] to evaluate.
        start: Starting x value.
        stop: Final x value.
        steps: Number of samples to generate.
        rate: Multiply the input domain by this value.
        phase: Offset the input domain by this value.
        mul: Multiply output by this value.
        offset: Offset output by this value.
    """

    abbreviation = "punary"

    def __init__(self,
                 function: Callable[[float], float],
                 start: float = 0.0,
                 stop: float = 1.0,
                 steps: int = 100,
                 rate: float = 1.0,
                 phase: float = 0.0,
                 mul: float = 1.0,
                 offset: float = 0.0):
        self.function = function
        self.start = start
        self.stop = stop
        self.steps = steps
        self.rate = rate
        self.phase = phase
        self.mul = mul
        self.offset = offset
        self.reset()

    def __repr__(self):
        return (
            f"PUnaryFunction({self.function}, {self.start}, {self.stop}, "
            f"{self.steps}, rate={self.rate}, phase={self.phase}, "
            f"mul={self.mul}, offset={self.offset})"
        )

    def reset(self):
        super().reset()
        self.index = 0

    def __next__(self):
        steps = Pattern.value(self.steps)
        if self.index >= steps:
            raise StopIteration
        start = Pattern.value(self.start)
        stop = Pattern.value(self.stop)
        fn = self.function
        if steps <= 1:
            x = start
        else:
            x = start + (stop - start) * float(self.index) / float(steps - 1)
        rate = Pattern.value(self.rate)
        phase = Pattern.value(self.phase)
        x = x * rate + phase
        self.index += 1
        value = fn(x)
        mul = Pattern.value(self.mul)
        offset = Pattern.value(self.offset)
        return value * mul + offset


class PCallableUnaryFunction(Pattern):
    """Sample a unary function where parameters are callables.

    Args:
        function: Callable[[float], float] to evaluate.
        start: Callable returning the starting x value for each step.
        stop: Callable returning the final x value for each step.
        steps: Number of samples to generate.
        rate: Callable returning a rate multiplier for the input domain.
        phase: Callable returning a phase offset for the input domain.
        mul: Callable returning an output multiplier.
        offset: Callable returning an output offset.
    """

    abbreviation = "pcallunary"

    def __init__(self,
                 function: Callable[[float], float],
                 start: Callable[[float], float] = lambda t: 0.0,
                 stop: Callable[[float], float] = lambda t: 1.0,
                 steps: int = 100,
                 rate: Callable[[float], float] = lambda t: 1.0,
                 phase: Callable[[float], float] = lambda t: 0.0,
                 mul: Callable[[float], float] = lambda t: 1.0,
                 offset: Callable[[float], float] = lambda t: 0.0):
        self.function = function
        self.start = start
        self.stop = stop
        self.steps = steps
        self.rate = rate
        self.phase = phase
        self.mul = mul
        self.offset = offset
        self.reset()

    def __repr__(self):
        return (
            f"PCallableUnaryFunction({self.function}, {self.start}, {self.stop}, "
            f"{self.steps}, rate={self.rate}, phase={self.phase}, "
            f"mul={self.mul}, offset={self.offset})"
        )

    def reset(self):
        super().reset()
        self.index = 0

    def __next__(self):
        steps = Pattern.value(self.steps)
        if self.index >= steps:
            raise StopIteration
        if steps <= 1:
            t = 0.0
        else:
            t = float(self.index) / float(steps - 1)
        start = self.start(t)
        stop = self.stop(t)
        if steps <= 1:
            x = start
        else:
            x = start + (stop - start) * t
        rate = self.rate(t)
        phase = self.phase(t)
        x = x * rate + phase
        self.index += 1
        value = self.function(x)
        mul = self.mul(t)
        offset = self.offset(t)
        return value * mul + offset

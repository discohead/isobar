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
                 start: Callable[[float], float] | float | Pattern = 0.0,
                 stop: Callable[[float], float] | float | Pattern = 1.0,
                 steps: int = 100,
                 rate: Callable[[float], float] | float | Pattern = 1.0,
                 phase: Callable[[float], float] | float | Pattern = 0.0,
                 mul: Callable[[float], float] | float | Pattern = 1.0,
                 offset: Callable[[float], float] | float | Pattern = 0.0):
        self.function = function
        self.start = start
        self._start_callable = callable(start)
        self.stop = stop
        self._stop_callable = callable(stop)
        self.steps = steps
        self.rate = rate
        self._rate_callable = callable(rate)
        self.phase = phase
        self._phase_callable = callable(phase)
        self.mul = mul
        self._mul_callable = callable(mul)
        self.offset = offset
        self._offset_callable = callable(offset)
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

        if steps <= 1:
            t = 0.0
        else:
            t = float(self.index) / float(steps - 1)

        if self._start_callable:
            start = self.start(t)
        else:
            start = Pattern.value(self.start)

        if self._stop_callable:
            stop = self.stop(t)
        else:
            stop = Pattern.value(self.stop)

        if steps <= 1:
            x = start
        else:
            x = start + (stop - start) * t

        if self._rate_callable:
            rate = self.rate(t)
        else:
            rate = Pattern.value(self.rate)

        if self._phase_callable:
            phase = self.phase(t)
        else:
            phase = Pattern.value(self.phase)

        x = x * rate + phase

        self.index += 1
        value = self.function(x)

        if self._mul_callable:
            mul = self.mul(t)
        else:
            mul = Pattern.value(self.mul)

        if self._offset_callable:
            offset = self.offset(t)
        else:
            offset = Pattern.value(self.offset)

        return value * mul + offset


class PCallableUnaryFunction(PUnaryFunction):
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
        for name, value in {
            'start': start,
            'stop': stop,
            'rate': rate,
            'phase': phase,
            'mul': mul,
            'offset': offset,
        }.items():
            if not callable(value):
                raise TypeError(f"{name} must be callable")

        super().__init__(
            function,
            start=start,
            stop=stop,
            steps=steps,
            rate=rate,
            phase=phase,
            mul=mul,
            offset=offset,
        )


# Python-Specific Patterns in Isobar

## Modern Python Features Used

### Type Hints (Python 3.5+)
```python
from typing import Iterable, Callable, Any, Optional, Union

def __init__(self,
             tempo: float = DEFAULT_TEMPO,
             output_device: Any = None,
             clock_source: Any = None,
             ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT):
```

### Dataclasses (Python 3.7+)
```python
from dataclasses import dataclass

@dataclass
class Action:
    time: float
    function: Callable
```

### Future Annotations (Python 3.7+)
```python
from __future__ import annotations
```
Enables forward references in type hints.

### F-Strings (Python 3.6+)
```python
log.info(f"Starting timeline with tempo {self.tempo}")
```

## Iterator Protocol Implementation

### Basic Pattern Iterator
```python
class Pattern:
    def __iter__(self):
        return self
    
    def __next__(self):
        # Must be implemented by subclasses
        raise NotImplementedError
    
    def reset(self):
        # Reset to initial state
        pass
```

### Generator Functions
```python
def pattern_generator():
    index = 0
    while True:
        yield values[index % len(values)]
        index += 1
```

## Property Decorators

### Read-Only Properties
```python
@property
def current_tempo(self):
    """Current tempo in BPM"""
    return self._tempo

@property
def ticks_per_beat(self):
    return self._ticks_per_beat
```

### Computed Properties
```python
@property
def seconds_per_tick(self):
    return 60.0 / (self.tempo * self.ticks_per_beat)
```

## Context Managers

### Resource Management
```python
class MidiOutputDevice:
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
```

## Operator Overloading Patterns

### Arithmetic Operators
```python
def __add__(self, operand):
    """Binary op: add two patterns"""
    return PAdd(self, operand)

def __radd__(self, operand):
    """Reverse add for commutative operations"""
    return self.__add__(operand)
```

### Comparison Operators
```python
def __eq__(self, other):
    return PEqual(self, other)

def __lt__(self, other):
    return PLessThan(self, other)
```

## Exception Handling Patterns

### Custom Exceptions
```python
class TrackLimitReachedException(Exception):
    """Raised when max_tracks limit exceeded"""
    pass

class InvalidMIDIChannelException(Exception):
    """Raised for invalid MIDI channel (0-15)"""
    pass
```

### Graceful Degradation
```python
try:
    import rtmidi
    MIDI_AVAILABLE = True
except ImportError:
    log.warning("python-rtmidi not installed")
    MIDI_AVAILABLE = False
```

## Module Organization

### Package Initialization
```python
# __init__.py
from .core import Pattern
from .sequence import PSequence, PLoop, PSeries
from .chance import PRandom, PWhite, PBrown

__all__ = ['Pattern', 'PSequence', 'PLoop', 'PSeries', 
           'PRandom', 'PWhite', 'PBrown']
```

### Lazy Imports
```python
def get_midi_output():
    global MidiOutputDevice
    if MidiOutputDevice is None:
        from .midi.output import MidiOutputDevice
    return MidiOutputDevice
```

## Class Method Types

### Static Methods
```python
@staticmethod
def value(v):
    """Extract scalar value from pattern or return as-is"""
    if isinstance(v, Pattern):
        return next(v)
    return v
```

### Class Methods
```python
@classmethod
def from_string(cls, notation: str):
    """Create pattern from string notation"""
    return cls(parse_notation(notation))
```

## Metaclass Usage

### Pattern Registration
```python
class PatternMeta(type):
    """Metaclass to register pattern abbreviations"""
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if 'abbreviation' in attrs:
            register_pattern(attrs['abbreviation'], cls)
        return cls
```

## Threading Patterns

### Thread-Safe Operations
```python
import threading

class Timeline:
    def __init__(self):
        self._lock = threading.RLock()
        self._running = False
    
    def add_track(self, track):
        with self._lock:
            self.tracks.append(track)
```

### Background Threads
```python
def run(self):
    self._thread = threading.Thread(target=self._run_thread)
    self._thread.daemon = True
    self._thread.start()
```

## Iteration Helpers

### Using itertools
```python
import itertools

def all(self, count=None):
    """Return all values up to count"""
    if count is None:
        items = list(self)
    else:
        items = list(itertools.islice(self, count))
    self.reset()
    return items
```

### Chain Patterns
```python
def __or__(self, other):
    """Concatenate patterns with | operator"""
    return PConcat([self, other])
```

## Duck Typing

### Flexible Input Handling
```python
def __init__(self, sequence):
    # Accept any iterable
    if hasattr(sequence, '__iter__'):
        self.sequence = list(sequence)
    else:
        self.sequence = [sequence]
```

## Debugging Support

### repr() Implementation
```python
def __repr__(self):
    """Return reconstructable representation"""
    return f"PSequence({self.sequence!r}, {self.repeats})"
```

### Logging Integration
```python
import logging
log = logging.getLogger(__name__)

def process_event(self, event):
    log.debug(f"Processing event: {event}")
```

## Performance Patterns

### Lazy Evaluation
```python
class PRange(Pattern):
    def __init__(self, start, stop, step=1):
        # Don't generate values until needed
        self.start = start
        self.stop = stop
        self.step = step
```

### Memoization
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def midi_note_to_frequency(note):
    return 440.0 * pow(2, (note - 69) / 12.0)
```

## Testing Patterns

### Pytest Fixtures
```python
import pytest

@pytest.fixture
def timeline():
    """Provide a test timeline"""
    return Timeline(tempo=120)

def test_timeline_tempo(timeline):
    assert timeline.tempo == 120
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 6),
    ([0, 0, 0], 0),
    ([], 0)
])
def test_pattern_sum(input, expected):
    p = PSequence(input)
    assert sum(p.all()) == expected
```
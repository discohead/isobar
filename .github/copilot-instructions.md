# Copilot Instructions for isobar

You are working on isobar, a Python library for algorithmic music composition using pattern generators.

## Core Patterns

### Pattern Classes
- ALL patterns start with 'P': `PSequence`, `PRandom`, `PMarkov`
- Inherit from `Pattern` base class
- Implement iterator protocol: `__next__()`, `reset()`
- Include `abbreviation = "pname"` for shorthand

### Pattern Structure
```python
class PNewPattern(Pattern):
    abbreviation = "pnew"
    
    def __init__(self, param):
        self.param = param
        self.reset()
    
    def __next__(self):
        param = Pattern.value(self.param)  # Handle nested patterns
        # Logic here
        return value
    
    def reset(self):
        super().reset()
        # Reset state
```

### Event Scheduling
```python
timeline.schedule({
    "note": pattern_or_value,      # 0-127
    "duration": pattern_or_value,   # in beats
    "velocity": pattern_or_value,   # 0-127
    "channel": 0-15
})
```

## Key Conventions

### Imports
```python
from __future__ import annotations
import logging
log = logging.getLogger(__name__)
```

### MIDI Validation
```python
note = int(note) % 128      # 0-127
velocity = int(velocity) % 128
channel = int(channel) % 16  # 0-15
```

### Testing Pattern
```python
def test_pattern_name():
    p = iso.PPattern(args)
    assert next(p) == expected
    assert p.all(4) == [1, 2, 3, 4]
```

## Common Patterns

### Euclidean Rhythms
```python
PBjorklund(hits, steps)  # e.g., 5 hits in 16 steps
```

### Random Variations
```python
PGaussian(mean, deviation)
PChoice([values], weights=[probabilities])
PBrown(min, max, step)  # Brownian motion
```

### Sequence Operations
```python
pattern + 12           # Transpose
pattern * 2            # Scale values
pattern % 12           # Wrap to octave
PConcat([p1, p2])     # Concatenate
```

## Output Devices
All inherit from `OutputDevice` with methods:
- `note_on(note, velocity, channel)`
- `note_off(note, channel)`
- `control(cc, value, channel)`

## Architecture Rules
- Patterns are pure iterators (no timeline/output knowledge)
- Timeline manages tracks and tempo
- Events flow: Pattern → Track → Timeline → OutputDevice
- Default timing: 480 PPQN
- Use `ignore_exceptions=True` for live coding
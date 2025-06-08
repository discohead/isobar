# Discovered Patterns in Isobar Codebase

## Naming Conventions

### Classes
- **Pattern Classes**: PascalCase with 'P' prefix for pattern types
  - `PSequence`, `PRange`, `PRandom`, `PMarkov`
  - Abbreviations stored in `abbreviation` class attribute
- **System Classes**: Standard PascalCase
  - `Timeline`, `Track`, `Clock`, `OutputDevice`
- **Event Classes**: Descriptive names with 'Event' suffix
  - `NoteEvent`, `ControlEvent`, `ActionEvent`

### Methods and Functions
- **Public Methods**: snake_case
  - `note_on()`, `note_off()`, `all_notes_off()`
  - `schedule()`, `run()`, `stop()`
- **Private Methods**: Leading underscore
  - `_tick()`, `_process_event()`, `_update_state()`
- **Property Methods**: Snake_case with @property decorator
  - `@property def ticks_per_beat(self)`

### Variables
- **Instance Variables**: snake_case
  - `self.sequence`, `self.repeats`, `self.current_time`
- **Class Constants**: UPPER_SNAKE_CASE
  - `LENGTH_MAX = 65536`
  - `DEFAULT_TEMPO = 120`
  - `DEFAULT_TICKS_PER_BEAT = 480`

### Module Structure
- **Public API**: Exposed via `__init__.py`
- **Internal Modules**: Leading underscore discouraged; use subpackages

## Core Design Patterns

### 1. Iterator Pattern (Fundamental)
```python
class Pattern:
    def __next__(self):
        # Generate next value
        pass
    
    def reset(self):
        # Reset to initial state
        pass
```
Every pattern implements this interface, enabling:
- Lazy evaluation
- Infinite sequences
- Composability

### 2. Operator Overloading for Composition
```python
def __add__(self, operand):
    return PAdd(self, operand)

def __mul__(self, operand):
    return PMul(self, operand)
```
Allows intuitive pattern math: `pattern1 + pattern2`

### 3. Static Value Coercion
```python
@staticmethod
def value(v):
    """Coerce a value to its scalar equivalent"""
    if isinstance(v, Pattern):
        return next(v)
    return v
```
Seamlessly handles both static values and patterns.

### 4. Factory Method Pattern
```python
@staticmethod
def pattern(v):
    """Convert value to Pattern if needed"""
    if isinstance(v, Pattern):
        return v
    else:
        return PConst(v)
```

### 5. Dataclass Usage (Modern Python)
```python
@dataclass
class Action:
    time: float
    function: Callable
```
Used for simple data containers with type hints.

## Code Organization Patterns

### Module Imports
1. **Future imports first**: `from __future__ import annotations`
2. **Standard library**: `import sys, math, copy, random`
3. **Type hints**: `from typing import Iterable, Callable, Any`
4. **Local imports**: Relative imports with dots
5. **Logger setup**: `log = logging.getLogger(__name__)`

### Class Structure
```python
class PatternClass(Pattern):
    """Docstring with description and example"""
    
    abbreviation = "pabbr"  # Shorthand notation
    
    def __init__(self, ...):
        # Validate inputs
        # Store parameters
        # Call reset()
    
    def __repr__(self):
        # Return constructor-style representation
    
    def reset(self):
        super().reset()
        # Reset internal state
    
    def __next__(self):
        # Core iteration logic
```

### Error Handling
- Custom exceptions in `exceptions.py`
- Graceful degradation with `ignore_exceptions` flag
- Proper cleanup in Timeline stop/shutdown

### Testing Patterns
```python
def test_pattern_basic():
    p = iso.PSequence([1, 2, 3], 1)
    assert next(p) == 1
    assert p.all() == [1, 2, 3]
    
def test_pattern_operators():
    p1 = iso.PSequence([1, 2], 1)
    p2 = iso.PSequence([3, 4], 1)
    p = p1 + p2
    assert p.all() == [4, 6]
```

## Documentation Patterns

### Docstring Format
```python
def method(self, param: type) -> return_type:
    """
    Brief description of method purpose.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this occurs
    """
```

### Inline Examples
Many classes include usage examples in docstrings:
```python
"""
>>> p = PSeq([1, 2, 3, 5])
>>> p.nextn(10)
[1, 2, 3, 5, 1, 2, 3, 5, 1, 2]
"""
```

## Common Idioms

### Pattern Reset Protection
```python
def all(self, count=None):
    # Store state
    items = list(itertools.islice(self, count))
    # Reset for next use
    self.reset()
    return items
```

### Default Parameter Handling
```python
if clock_source is None:
    clock_source = Clock(self, tempo, ticks_per_beat)
```

### Lazy Import for Optional Dependencies
```python
try:
    import rtmidi
except ImportError:
    log.warning("rtmidi not installed")
```

## Architecture Principles

1. **Separation of Concerns**: Pattern generation separate from output
2. **Pluggable I/O**: All outputs implement `OutputDevice` interface
3. **Event-Driven**: Timeline schedules events, devices handle them
4. **High Resolution**: 480 PPQN allows ~1ms timing precision
5. **Thread Safety**: Background threads for real-time operation
6. **State Management**: Global state in `globals/` for IPC
# CLAUDE.md - isobar/pattern

This directory contains the core pattern generation system - the heart of isobar's algorithmic composition capabilities.

## Module Overview

The `pattern` module implements the Pattern class hierarchy, providing dozens of pattern types for generating musical sequences. All patterns follow Python's iterator protocol and support mathematical operations through operator overloading.

## Core Architecture

### core.py
- **Base Class**: `Pattern` - Abstract base for all patterns
- **Key Methods**:
  - `__next__()`: Iterator protocol (must be implemented)
  - `reset()`: Reset pattern to initial state
  - `all(count)`: Get all values up to count
  - `value(v)`: Static method to extract scalar from pattern/value
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `%`, `**`) and comparison operators
- **Pattern Types**:
  - `PConstant`: Fixed value
  - `PRef`: Mutable pattern reference
  - `PFunc`: Function-based generation
  - `PDict/PDictKey`: Dictionary operations
  - All arithmetic operator patterns (`PAdd`, `PMul`, etc.)

## Pattern Categories

### Sequence Patterns (sequence.py)
- **Linear**: `PSeries`, `PRange`, `PGeom`
- **Looping**: `PLoop`, `PPingPong`, `PCreep`
- **Transformation**: `PStutter`, `PSubsequence`, `PReverse`
- **Rhythmic**: `PEuclidean`, `PImpulse`
- **Advanced**: `PArpeggiator`, `PPermut`

### Stochastic Patterns (chance.py)
- **Random**: `PWhite`, `PBrown`, `PRandomExponential`
- **Choice**: `PChoice`, `PSample`, `PShuffle`
- **Probability**: `PCoin`, `PSkip`, `PFlipFlop`
- **Structured**: `PWalk`, `PSwitchOne`

### Musical Patterns (tonal.py)
- **Scale-based**: `PDegree`, `PFilterByKey`, `PNearestNoteInKey`
- **Conversion**: `PMidiNoteToFrequency`

### Transformation Patterns (scalar.py)
- **Detection**: `PChanged`, `PDiff`
- **Mapping**: `PMap`, `PMapEnumerated`
- **Scaling**: `PScaleLinLin`, `PScaleLinExp`
- **Processing**: `PNormalise`, `PWrap`, `PRound`

### Time Patterns (warp.py)
- **Interpolation**: `PWInterpolate`
- **Modulation**: `PWSine`
- **Tempo**: `PWRallantando`

### Advanced Generators
- **markov.py**: `PMarkov` - First-order Markov chains
- **lsystem.py**: `PLSystem` - Lindenmayer systems
- **fade.py**: `PFadeNotewise`, `PFadeNotewiseRandom`
- **oscillator.py**: Oscillator-based patterns
- **midi.py**: MIDI-specific patterns
- **static.py**: `PGlobals`, `PCurrentTime`

## Pattern Creation Template

```python
class PYourPattern(Pattern):
    """Brief description.
    
    Detailed explanation of what the pattern does.
    
    Args:
        param1: Description
        param2: Description
        
    Examples:
        >>> p = PYourPattern(param1, param2)
        >>> p.all(8)
        [1, 2, 3, 4, 5, 6, 7, 8]
    """
    
    abbreviation = "pyour"  # For shorthand notation
    
    def __init__(self, param1, param2=None):
        # Validate parameters
        if param2 is None:
            param2 = default_value
            
        # Store parameters
        self.param1 = param1
        self.param2 = param2
        
        # Always call reset
        self.reset()
    
    def __repr__(self):
        # Return reconstructable representation
        return f"PYourPattern({self.param1!r}, {self.param2!r})"
    
    def reset(self):
        # Call parent reset
        super().reset()
        
        # Reset internal state
        self.index = 0
        self.current_value = None
    
    def __next__(self):
        # Extract values from parameters (may be patterns)
        value1 = Pattern.value(self.param1)
        value2 = Pattern.value(self.param2)
        
        # Your generation logic here
        result = compute_next_value(value1, value2, self.index)
        
        # Update state
        self.index += 1
        
        # Return result
        return result
```

## Key Design Principles

1. **Lazy Evaluation**: Patterns generate values only when requested
2. **Composability**: Patterns can contain other patterns
3. **Immutability**: Pattern parameters shouldn't change after creation
4. **Resettable**: All patterns must implement proper reset behavior
5. **Operator Support**: Use operator overloading for intuitive syntax

## Common Implementation Patterns

### Parameter Handling
```python
def __init__(self, sequence, repeats=None):
    # Handle infinite repeats
    if repeats is None:
        repeats = Pattern.LENGTH_MAX
    
    # Convert to list if needed
    if hasattr(sequence, '__iter__'):
        self.sequence = list(sequence)
    else:
        self.sequence = [sequence]
```

### Value Extraction
```python
def __next__(self):
    # Get scalar value from pattern or static value
    step = Pattern.value(self.step)
    
    # Use the value
    self.current += step
```

### Finite Pattern Handling
```python
def __next__(self):
    if self.count >= self.max_count:
        raise StopIteration
    
    value = self.generate_value()
    self.count += 1
    return value
```

### Reset Implementation
```python
def reset(self):
    super().reset()  # Always call parent
    
    # Reset counters
    self.index = 0
    self.count = 0
    
    # Reset nested patterns
    if isinstance(self.nested, Pattern):
        self.nested.reset()
```

## Testing Patterns

### Basic Functionality
```python
def test_pattern_basic():
    p = PYourPattern(param)
    assert next(p) == expected_first
    assert p.all(4) == [1, 2, 3, 4]
```

### Reset Behavior
```python
def test_pattern_reset():
    p = PYourPattern(param)
    first_run = p.all(4)
    second_run = p.all(4)
    assert first_run == second_run
```

### Operator Overloading
```python
def test_pattern_operators():
    p1 = PSequence([1, 2])
    p2 = PSequence([3, 4])
    p_sum = p1 + p2
    assert p_sum.all() == [4, 6]
```

### Edge Cases
```python
def test_pattern_edge_cases():
    # Empty sequences
    p = PSequence([])
    assert p.all() == []
    
    # Single values
    p = PYourPattern(42)
    assert next(p) == 42
```

## Performance Considerations

1. **Memory**: Use generators/iterators, not pre-computed lists
2. **CPU**: Minimize computation in `__next__()`
3. **Caching**: Cache expensive computations when appropriate
4. **State**: Keep state minimal for fast reset

## Common Pitfalls

1. **Forgetting reset()**: Always call in `__init__`
2. **Mutable state**: Don't modify pattern parameters
3. **Missing super().reset()**: Break the reset chain
4. **Non-deterministic behavior**: Use seed for reproducibility
5. **Infinite recursion**: Be careful with nested patterns

## Related Modules

- `timelines/`: Schedules pattern-generated events
- `shorthand/`: Abbreviated pattern creation
- `notation/`: String-based pattern input
- `io/`: Output devices that receive pattern values
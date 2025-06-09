# AGENTS.md - isobar/pattern

## Module Overview
Core pattern generation system - the heart of isobar. All patterns implement Python iterator protocol and support operator overloading for composition.

## AI Context Integration
- **Architecture guide**: See `CLAUDE.md` in this directory
- **Pattern conventions**: Check `.cursor/rules/components/patterns.mdc`
- **Implementation template**: See `.github/instructions/pattern-creation.md`
- **Workflow guide**: See `claude/workflows/creating-patterns.md`

## Key Files
- `core.py` - Base `Pattern` class and operators
- `sequence.py` - Sequential patterns (PSequence, PLoop, etc.)
- `chance.py` - Stochastic patterns (PRandom, PChoice, etc.)
- `tonal.py` - Musical patterns (PDegree, etc.)
- `scalar.py` - Value transformations

## Development Commands
```bash
# Run all pattern tests
pytest tests/test_pattern*.py -v

# Test specific pattern category
pytest tests/test_pattern_chance.py
pytest tests/test_pattern_sequence.py

# Quick pattern testing
python -c "from isobar import *; print(PSequence([1,2,3]).all())"

# Test operator overloading
python -c "from isobar import *; p = PSequence([1,2]) + 10; print(p.all())"
```

## Creating a New Pattern

### Step 1: Create pattern class
```python
# In appropriate module file
class PYourPattern(Pattern):
    abbreviation = "pyour"  # REQUIRED for shorthand
    
    def __init__(self, param):
        self.param = param
        self.reset()  # ALWAYS call reset
    
    def __next__(self):
        value = Pattern.value(self.param)  # Extract scalar
        # Your logic here
        return result
    
    def reset(self):
        super().reset()  # ALWAYS call super
        self.index = 0
```

### Step 2: Add tests
```python
# In tests/test_pattern_yourtype.py
def test_your_pattern_basic():
    p = PYourPattern(param)
    assert next(p) == expected
    assert p.all(4) == [1, 2, 3, 4]

def test_your_pattern_reset():
    p = PYourPattern(param)
    first = p.all(4)
    second = p.all(4)
    assert first == second
```

### Step 3: Register abbreviation
```python
# In __init__.py
from .yourmodule import PYourPattern
__all__.append('PYourPattern')
```

## Common Pattern Categories

### Sequence patterns (sequence.py)
- `PSequence` - Basic sequence
- `PLoop` - Looping sequence  
- `PEuclidean` - Euclidean rhythms
- `PArpeggiator` - Arpeggiator patterns

### Random patterns (chance.py)
- `PRandom` - Uniform random
- `PBrown` - Brownian motion
- `PChoice` - Weighted choice
- `PShuffle` - Shuffled sequence

### Musical patterns (tonal.py)
- `PDegree` - Scale degrees
- `PFilterByKey` - Key filtering

## Code Pointers
- Base class: `Pattern` in `core.py` lines 50-200
- Iterator protocol: `__next__()` and `reset()` methods
- Operator overloading: `__add__`, `__mul__` etc. in `core.py`
- Value extraction: `Pattern.value()` static method

## Testing Patterns
```bash
# Test in isolation
python -c "
from isobar import *
p = PYourPattern(args)
print('First 10:', p.all(10))
print('Reset works:', p.all(10))
"

# Test with timeline
python examples/test_pattern.py
```

## Validation Steps
1. Pattern has `abbreviation` attribute
2. `__init__` calls `self.reset()`
3. `reset()` calls `super().reset()`
4. `__next__` uses `Pattern.value()` for nested patterns
5. Operators return new Pattern instances
6. Tests cover basic, reset, and edge cases

## Common Issues
- Forgetting `self.reset()` in `__init__`
- Not calling `super().reset()`
- Mutating pattern state instead of creating new patterns
- Not handling `StopIteration` for finite patterns
- Missing `abbreviation` for shorthand
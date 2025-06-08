# Create New Pattern Class

<task>
Create a new pattern class following isobar conventions and patterns.
</task>

<context>
When creating a new pattern class in isobar, follow these established conventions:
1. Inherit from Pattern base class
2. Use P prefix for class name
3. Include abbreviation for shorthand notation
4. Implement iterator protocol
5. Support operator overloading
6. Include docstring with examples
</context>

<template>
```python
from __future__ import annotations
from typing import Any
from .core import Pattern

class PYourPattern(Pattern):
    """
    Brief description of what this pattern does.
    
    Longer explanation with details about behavior and use cases.
    
    Examples:
        >>> p = PYourPattern(param1, param2)
        >>> p.nextn(8)
        [1, 2, 3, 4, 5, 6, 7, 8]
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    """
    
    abbreviation = "pyour"
    
    def __init__(self, param1: Any, param2: Any = None):
        """Initialize the pattern with given parameters."""
        self.param1 = param1
        self.param2 = param2 if param2 is not None else default_value
        
        # Validate inputs
        if not valid_condition:
            raise ValueError("Error message")
            
        self.reset()
    
    def __repr__(self):
        return f"PYourPattern({self.param1!r}, {self.param2!r})"
    
    def reset(self):
        """Reset pattern to initial state."""
        super().reset()
        self.current_index = 0
        self.internal_state = self._initialize_state()
    
    def __next__(self):
        """Generate next value in the pattern."""
        # Handle pattern parameters that might be patterns themselves
        param1 = Pattern.value(self.param1)
        param2 = Pattern.value(self.param2)
        
        # Your pattern logic here
        if self.should_stop():
            raise StopIteration
            
        value = self._calculate_next_value()
        self._update_state()
        
        return value
    
    def _initialize_state(self):
        """Initialize internal state (private method)."""
        return {}
    
    def _calculate_next_value(self):
        """Calculate the next value based on current state."""
        # Implementation here
        return 0
    
    def _update_state(self):
        """Update internal state after generating a value."""
        self.current_index += 1
    
    def should_stop(self):
        """Check if pattern should stop iterating."""
        return False  # or your stop condition
```
</template>

<steps>
1. Create new file in `isobar/pattern/` directory
2. Add imports and Pattern base class inheritance
3. Write comprehensive docstring with examples
4. Define abbreviation for shorthand notation
5. Implement __init__ with parameter validation
6. Implement __repr__ for debugging
7. Implement reset() to initialize/reset state
8. Implement __next__ with pattern logic
9. Add helper methods as needed (prefix with _)
10. Add to `isobar/pattern/__init__.py` exports
11. Create tests in `tests/test_pattern_yourtype.py`
12. Update documentation if needed
</steps>

<testing_template>
```python
import pytest
import isobar as iso

def test_pyourpattern_basic():
    """Test basic functionality."""
    p = iso.PYourPattern(param1_value)
    assert next(p) == expected_value
    assert p.all(4) == [val1, val2, val3, val4]

def test_pyourpattern_reset():
    """Test pattern reset."""
    p = iso.PYourPattern(param1_value)
    next(p)
    next(p)
    p.reset()
    assert next(p) == first_value

def test_pyourpattern_operators():
    """Test operator overloading."""
    p1 = iso.PYourPattern(param1)
    p2 = p1 + 10
    assert next(p2) == expected_value + 10

def test_pyourpattern_edge_cases():
    """Test edge cases and error handling."""
    with pytest.raises(ValueError):
        iso.PYourPattern(invalid_param)
    
    # Test empty/zero cases
    p = iso.PYourPattern(edge_case_param)
    with pytest.raises(StopIteration):
        next(p)
```
</testing_template>
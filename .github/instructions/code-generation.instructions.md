# Code Generation Instructions

When generating code for isobar:

## Pattern Implementation
```python
# ALWAYS use this structure:
class PPatternName(Pattern):
    """Brief description."""
    abbreviation = "pname"
    
    def __init__(self, ...):
        # Validate inputs
        # Store parameters
        self.reset()
    
    def __repr__(self):
        return f"PPatternName({self.param!r})"
    
    def reset(self):
        super().reset()
        # Initialize state
    
    def __next__(self):
        # Extract values from patterns
        value = Pattern.value(self.param)
        
        # Core logic
        if done:
            raise StopIteration
            
        return result
```

## Timeline Usage
```python
# Create timeline
timeline = Timeline(tempo=120)

# Schedule events
timeline.schedule({
    "note": PSequence([60, 64, 67]),
    "duration": 0.5,
    "velocity": PGaussian(64, 10)
})

# Run
timeline.run()
```

## Pattern Operators
```python
# Support these operations:
p1 + p2    # Addition
p1 - p2    # Subtraction  
p1 * p2    # Multiplication
p1 / p2    # Division
p1 % p2    # Modulo
p1 ** p2   # Power
```

## Common Helpers
```python
# Pattern factory
@staticmethod
def pattern(value):
    if isinstance(value, Pattern):
        return value
    return PConstant(value)

# Value extraction
@staticmethod
def value(v):
    if isinstance(v, Pattern):
        return next(v)
    return v
```
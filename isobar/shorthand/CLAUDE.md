# CLAUDE.md - isobar/shorthand

This directory contains the shorthand notation system for rapid pattern creation and live coding.

## Module Overview

The `shorthand` module provides abbreviated syntax for creating patterns quickly, making isobar more suitable for live coding and interactive composition. It maps short abbreviations to full pattern class names.

## Core Components

### abbreviations.py
- **Purpose**: Define and manage pattern abbreviations
- **Key Data**: Maps abbreviations to pattern classes
- **Examples**:
  ```python
  "seq" → PSequence
  "rnd" → PRandom  
  "eu" → PEuclidean
  "ch" → PChoice
  ```

### setup.py
- **Purpose**: Initialize shorthand system and inject into namespace
- **Key Functions**:
  - `setup_shorthand()`: Install abbreviations globally
  - `create_shorthand_function()`: Generate shorthand constructors
  - `register_abbreviation()`: Add new abbreviations

### patches.py
- **Purpose**: Manage reusable pattern configurations (patches)
- **Key Features**:
  - Save/load pattern presets
  - Named patch registry
  - Patch interpolation

### sync.py
- **Purpose**: Synchronize shorthand definitions across processes
- **Key Features**:
  - Share abbreviations between instances
  - Network shorthand sync
  - Dynamic abbreviation updates

## Shorthand Syntax

### Basic Usage
```python
# Without shorthand
pattern = PSequence([60, 64, 67], 2)

# With shorthand
pattern = seq([60, 64, 67], 2)
```

### Common Abbreviations
```python
# Sequence patterns
seq([1, 2, 3])         # PSequence
ser(0, 1, 10)          # PSeries  
loop([1, 2, 3])        # PLoop

# Random patterns
rnd(0, 127)            # PRandom
wht(0, 127)            # PWhite
brn(60, 2)             # PBrown

# Choice patterns
ch([1, 2, 3])          # PChoice
shuf([1, 2, 3])        # PShuffle

# Rhythmic patterns
eu(5, 8)               # PEuclidean
imp(4)                 # PImpulse

# Musical patterns
deg([0, 2, 4], scale)  # PDegree
```

### Chaining Shortcuts
```python
# Chain patterns with operators
melody = seq([0, 2, 4, 5]) + ser(0, 12, 1)

# Combine with arithmetic
velocity = rnd(40, 80) + brn(0, 20, 2)
```

## Patch System

### Creating Patches
```python
# Define a patch
patches.register("bass_groove", {
    "note": seq([36, 36, 41, 43]),
    "duration": ch([0.5, 0.25, 0.25]),
    "velocity": rnd(70, 90)
})

# Use the patch
timeline.schedule(patches.get("bass_groove"))
```

### Patch Variations
```python
# Base patch
patches.register("arp_base", {
    "note": deg(ser(0, 1, 8), Scale.major),
    "duration": 0.125
})

# Variation
patches.register("arp_fast", 
    patches.get("arp_base").copy().update({
        "duration": 0.0625
    })
)
```

## Implementation Patterns

### Abbreviation Registration
```python
# In abbreviations.py
ABBREVIATIONS = {
    "seq": PSequence,
    "rnd": PRandom,
    "ch": PChoice,
    # ... more abbreviations
}

# Dynamic registration
def register_abbreviation(abbr, pattern_class):
    ABBREVIATIONS[abbr] = pattern_class
    
    # Create global function
    globals()[abbr] = create_shorthand_function(pattern_class)
```

### Shorthand Function Creation
```python
def create_shorthand_function(pattern_class):
    def shorthand_func(*args, **kwargs):
        return pattern_class(*args, **kwargs)
    
    # Preserve docstring and name
    shorthand_func.__doc__ = pattern_class.__doc__
    shorthand_func.__name__ = pattern_class.abbreviation
    
    return shorthand_func
```

### Namespace Injection
```python
def setup_shorthand():
    # Inject into global namespace
    import builtins
    
    for abbr, pattern_class in ABBREVIATIONS.items():
        func = create_shorthand_function(pattern_class)
        setattr(builtins, abbr, func)
```

## Live Coding Workflows

### Quick Pattern Building
```python
# Start simple
beat = seq([1, 0, 1, 0])

# Add variation
beat = ch([seq([1, 0, 1, 0]), seq([1, 1, 0, 0])])

# Add dynamics
beat = beat * rnd(0.7, 1.0)
```

### Rapid Iteration
```python
# Initial idea
timeline.schedule({"note": seq([60, 64, 67])})

# Quick modification
timeline.schedule({"note": shuf([60, 64, 67, 72])})

# Further development  
timeline.schedule({"note": ch([60, 64, 67, 72]) + brn(0, 12)})
```

## Best Practices

1. **Consistency**: Use standard abbreviations across projects
2. **Clarity**: Balance brevity with readability
3. **Documentation**: Document custom abbreviations
4. **Namespace**: Avoid conflicts with Python builtins

## Custom Abbreviations

### Adding Your Own
```python
# Register custom pattern
from isobar.pattern import Pattern

class PMyPattern(Pattern):
    abbreviation = "myp"
    # ... implementation

# Register shorthand
register_abbreviation("myp", PMyPattern)
```

### Project-Specific Shortcuts
```python
# Create domain-specific shortcuts
register_abbreviation("kick", lambda: PSequence([36]))
register_abbreviation("snare", lambda: PSequence([38]))
register_abbreviation("hihat", lambda: PSequence([42]))

# Use them
drums = kick() | rest(2) | snare() | rest(2)
```

## Integration Tips

### With Timeline
```python
t = Timeline(120)

# Shorthand makes scheduling concise
t.schedule({
    "note": deg(ser(0, 1, 8), Scale.minor) + 60,
    "duration": ch([0.25, 0.5]),
    "velocity": wht(40, 80)
})
```

### With Notation
```python
# Combine systems
melody = parse_notation("C D E F") + rnd(-12, 12)
```

## Testing Shorthand

```python
# Verify abbreviation mapping
assert seq([1, 2, 3]).all() == PSequence([1, 2, 3]).all()

# Test patch system
patches.register("test", {"note": seq([60])})
assert patches.get("test")["note"].all() == [60]
```

## Related Modules

- `pattern/`: Full pattern implementations
- `notation/`: String-based pattern creation
- `auxiliary/scripts/generate-shorthand-aliases.py`: Generate abbreviation docs
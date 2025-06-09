# AGENTS.md - isobar/shorthand

## Module Overview
Abbreviated syntax system for rapid pattern creation. Maps short names to pattern classes for live coding efficiency.

## AI Context Integration
- **System design**: See `CLAUDE.md` in this directory
- **Live coding patterns**: Check `.cursor/rules/workflows/live-coding.mdc`
- **Abbreviation guide**: See `.github/instructions/shorthand-usage.md`

## Key Files
- `abbreviations.py` - Pattern name mappings
- `setup.py` - Namespace injection logic
- `patches.py` - Reusable pattern configurations
- `sync.py` - Cross-process abbreviation sync

## Development Commands
```bash
# Generate abbreviation docs
python auxiliary/scripts/generate-shorthand-aliases.py

# Test shorthand setup
python -c "from isobar import *; setup_shorthand(); print(seq([1,2,3]).all())"

# List all abbreviations
python -c "from isobar.shorthand.abbreviations import ABBREVIATIONS; print(sorted(ABBREVIATIONS.keys()))"

# Test patch system
python -c "from isobar.shorthand.patches import patches; print(patches.list())"
```

## Adding New Abbreviations

### Step 1: Update abbreviations.py
```python
ABBREVIATIONS = {
    # ... existing ...
    "newp": PNewPattern,  # Add your abbreviation
}
```

### Step 2: Ensure pattern has abbreviation
```python
class PNewPattern(Pattern):
    abbreviation = "newp"  # Must match above
```

### Step 3: Test shorthand
```python
from isobar import *
setup_shorthand()
p = newp(args)  # Should work
```

## Working with Patches

### Creating a patch
```python
patches.register("drum_kit", {
    "kick": seq([36]),
    "snare": seq([38]),
    "hihat": ch([42, 44])
})
```

### Using patches
```python
kit = patches.get("drum_kit")
timeline.schedule({
    "note": kit["kick"],
    "duration": 1
})
```

## Common Abbreviations Reference
```python
# Sequences
seq([1,2,3])      # PSequence
loop([1,2,3])     # PLoop  
ser(0, 10, 2)     # PSeries

# Random
rnd(0, 127)       # PRandom
ch([1,2,3])       # PChoice
brn(60, 2)        # PBrown

# Musical
deg([0,2,4], scale)  # PDegree
eu(5, 8)             # PEuclidean
```

## Code Pointers
- Abbreviation map: `ABBREVIATIONS` dict in `abbreviations.py`
- Setup function: `setup_shorthand()` in `setup.py`
- Patch registry: `PatchRegistry` class in `patches.py`
- Function creation: `create_shorthand_function()` in `setup.py`

## Testing Shorthand

### Verify abbreviation works
```bash
python -c "
from isobar import *
setup_shorthand()

# Test each category
print('seq:', seq([1,2,3]).all())
print('rnd:', [next(rnd(0,10)) for _ in range(3)])
print('eu:', eu(3,8).all())
"
```

### Test patch system
```bash
python -c "
from isobar.shorthand.patches import patches

# Register test patch
patches.register('test', {'note': seq([60,64,67])})

# Verify it works
print(patches.get('test'))
print(patches.list())
"
```

## Validation Steps
1. All patterns have `abbreviation` attribute
2. Abbreviations are unique (no conflicts)
3. Shorthand functions preserve docstrings
4. Patches serialize/deserialize correctly
5. No namespace pollution

## Live Coding Tips
- Keep abbreviations short (2-4 chars)
- Use consistent naming schemes
- Create domain-specific shortcuts
- Leverage patches for common patterns
- Test abbreviations before performance

## Common Issues
- Abbreviation conflicts with Python builtins
- Pattern missing `abbreviation` attribute
- Namespace not properly initialized
- Patch registry not persisting
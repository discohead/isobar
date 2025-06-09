# AGENTS.md - isobar/notation

## Module Overview
Musical notation parsing system for converting human-readable strings into Pattern objects. Supports note names, chords, rhythms, and scale degrees.

## AI Context Integration
- **Parser details**: See `CLAUDE.md` in this directory
- **Notation syntax**: Check `.cursor/rules/features/notation.mdc`
- **Pattern integration**: See `.github/instructions/notation-patterns.md`

## Key Files
- `notation.py` - Main parser implementation
- `__init__.py` - Public API (`parse_notation()`)

## Development Commands
```bash
# Run notation tests
pytest tests/test_notation.py -v

# Test parser with examples
python -c "from isobar.notation import parse_notation; print(parse_notation('C4 E4 G4').all())"

# Validate chord parsing
python -c "from isobar.notation import parse_notation; print(parse_notation('Cmaj7 Dm7 G7').all())"
```

## Testing Instructions

### Adding notation features
1. Update regex patterns in `notation.py`
2. Add parsing logic to appropriate function
3. Create test cases in `tests/test_notation.py`
4. Update documentation with examples

### Common test patterns
```python
# Test note parsing
assert parse_notation("C4") == PSequence([60])

# Test chord symbols
assert parse_notation("C") == PSequence([[60, 64, 67]])

# Test with rhythm
notes, durations = parse_notation("C4:q D4:e E4:e")
```

## Notation Syntax Reference

### Basic elements
- Notes: `C4`, `D#5`, `Eb3`
- Chords: `C`, `Cm`, `C7`, `Cmaj7`
- Rests: `r`, `_`
- Rhythms: `q` (quarter), `e` (eighth), `h` (half)

### Advanced patterns
```python
# Mixed notation
"C4 _ D4 [E4,G4]"  # Note, rest, note, simultaneous notes

# With dynamics
"C4:mp D4:f E4:pp"  # mp, f, pp velocities
```

## Code Pointers
- Main parser: `parse_notation()` function
- Note parsing: `parse_note()` with regex `NOTE_REGEX`
- Chord parsing: `parse_chord()` with chord mappings
- Tokenizer: `tokenize()` function

## Common Tasks

### Extending chord vocabulary
1. Add chord definition to `CHORD_INTERVALS` dict
2. Update `parse_chord()` logic
3. Add test case
4. Document in syntax reference

### Debugging parsing issues
```python
# Enable debug mode
import logging
logging.getLogger('isobar.notation').setLevel(logging.DEBUG)

# Test individual components
from isobar.notation import parse_note, parse_chord
print(parse_note("C#4"))  # Should return 61
```

## Validation Steps
1. Run `pytest tests/test_notation.py`
2. Verify MIDI note ranges (0-127)
3. Test malformed input handling
4. Check chord interval accuracy
5. Validate rhythm duration values

## Error Handling
- Invalid notes raise `NotationError`
- Ambiguous syntax provides helpful messages
- Graceful fallback for unknown symbols
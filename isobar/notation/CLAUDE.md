# CLAUDE.md - isobar/notation

This directory contains the musical notation parsing system for human-readable pattern input.

## Module Overview

The `notation` module provides a parser for converting string-based musical notation into isobar patterns. This allows for more intuitive and compact pattern creation using familiar musical concepts.

## Core Component

### notation.py
- **Purpose**: Parse string notation into Pattern objects
- **Key Functions**:
  - `parse_notation()`: Main parsing function
  - `parse_note()`: Convert note names to MIDI numbers
  - `parse_rhythm()`: Parse rhythmic notation
  - `parse_degrees()`: Parse scale degree notation

## Notation Syntax

### Note Names
```python
# Standard note names
"C4"   → 60  # Middle C
"D#5"  → 75  # D sharp, octave 5
"Eb3"  → 51  # E flat, octave 3
"G-1"  → 19  # G, octave -1
```

### Chord Notation
```python
# Chord symbols
"C"    → [60, 64, 67]      # C major triad
"Cm"   → [60, 63, 67]      # C minor triad
"C7"   → [60, 64, 67, 70]  # C dominant 7th
"Cmaj7" → [60, 64, 67, 71] # C major 7th
```

### Scale Degrees
```python
# Roman numeral notation
"I"    → 0   # Tonic
"IV"   → 5   # Subdominant  
"V7"   → [7, 11, 14, 17]  # Dominant 7th chord
```

### Rhythmic Notation
```python
# Duration values
"q"    → 1.0   # Quarter note
"e"    → 0.5   # Eighth note
"s"    → 0.25  # Sixteenth note
"h"    → 2.0   # Half note
"w"    → 4.0   # Whole note
```

### Rest Notation
```python
# Rests
"r"    → None  # Rest
"_"    → None  # Alternative rest notation
```

## Usage Examples

### Basic Patterns
```python
# Parse a melodic sequence
pattern = parse_notation("C4 D4 E4 F4 G4")
# Returns: PSequence([60, 62, 64, 65, 67])

# With rhythm
pattern = parse_notation("C4:q D4:e E4:e F4:h")
# Returns note and duration patterns
```

### Chord Progressions
```python
# Parse chord symbols
progression = parse_notation("C G Am F")
# Returns: PSequence([[60,64,67], [67,71,74], [69,72,76], [65,69,72]])
```

### Advanced Notation
```python
# Mixed notation
pattern = parse_notation("C4 _ D4 [E4,G4] _")
# Includes rests and simultaneous notes

# With dynamics
pattern = parse_notation("C4:mp D4:f E4:pp")
# Parses velocity information
```

## Implementation Patterns

### Parser Structure
```python
def parse_notation(notation_string):
    tokens = tokenize(notation_string)
    elements = []
    
    for token in tokens:
        if is_note(token):
            elements.append(parse_note(token))
        elif is_chord(token):
            elements.append(parse_chord(token))
        elif is_rest(token):
            elements.append(None)
    
    return PSequence(elements)
```

### Note Parsing
```python
def parse_note(note_string):
    # Extract note name, octave, accidentals
    match = NOTE_REGEX.match(note_string)
    if match:
        note = match.group('note')
        octave = int(match.group('octave'))
        accidental = match.group('accidental')
        
        # Convert to MIDI number
        return note_to_midi(note, octave, accidental)
```

## Integration with Patterns

### Direct Usage
```python
from isobar.notation import parse_notation

melody = parse_notation("C4 E4 G4 C5")
timeline.schedule({
    "note": melody,
    "duration": 0.5
})
```

### With Shorthand
```python
# Notation can be used with shorthand system
n"C4 E4 G4" | n"F4 A4 C5"  # Concatenate notations
```

## Error Handling

- Invalid note names raise `NotationError`
- Malformed syntax provides helpful error messages
- Graceful handling of ambiguous notation

## Extensions

The notation system is designed to be extensible:
- Custom chord definitions
- Microtonal notation support
- Extended rhythm patterns
- Dynamic markings

## Best Practices

1. **Consistency**: Use consistent octave numbering
2. **Clarity**: Prefer explicit notation over ambiguous
3. **Validation**: Validate parsed output for MIDI range
4. **Documentation**: Document custom notation extensions

## Testing Notation

```python
# Test parsing
assert parse_notation("C4") == PSequence([60])
assert parse_notation("C4 D4 E4") == PSequence([60, 62, 64])
assert parse_notation("C") == PSequence([[60, 64, 67]])  # Chord
```

## Related Modules

- `pattern/`: Pattern classes that notation creates
- `note.py`: Note-to-MIDI conversion utilities
- `chord.py`: Chord construction from notation
- `scale.py`: Scale degree resolution
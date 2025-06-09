# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

isobar is a Python library for algorithmic composition, generative music, and sonification. It provides a framework for creating and manipulating musical patterns programmatically, with support for various output devices (MIDI, OSC, SuperCollider, FluidSynth).

## Development Commands

```bash
# Install for development
pip3 install -e .

# Run all tests
pytest

# Run tests with coverage
pytest --cov=isobar tests

# Run a single test file
pytest tests/test_pattern.py

# Run a specific test
pytest tests/test_pattern.py::TestPattern::test_pattern_basic

# Code style check
flake8 isobar

# Generate documentation
mkdocs serve

# Regenerate pattern library documentation
auxiliary/scripts/generate-docs.py -m > docs/patterns/library.md
```

## Architecture Overview

### Core Event Flow
1. **Timeline** controls tempo and scheduling
2. **Patterns** generate values based on musical rules
3. **Events** are created from pattern values
4. **OutputDevices** send events to external systems

### Key Modules

**Pattern System** (`pattern/`): All patterns inherit from `Pattern` base class and implement Python iterator protocol. Patterns support operator overloading for arithmetic operations and can be composed/nested.

**Timeline System** (`timelines/`): 
- `Timeline`: Main orchestrator, manages tracks and global tempo
- `Track`: Schedules events based on patterns
- `Clock`: Abstract base for different clock sources (internal, MIDI sync, Ableton Link)
- `Event`: Base class for `NoteEvent`, `ControlEvent`, etc.

**I/O System** (`io/`): Each output type implements `OutputDevice` interface with methods like `note_on()`, `note_off()`, `control()`. MIDI uses `mido` library, OSC uses `python-osc`.

**Music Theory** (`note.py`, `scale.py`, `chord.py`, `key.py`): Provides musical primitives with MIDI note number conversions and scale/chord operations.

### Pattern Categories
- **Core** (`core.py`): Arithmetic, logic, concatenation
- **Sequence** (`sequence.py`): Series, loops, arpeggiators, Euclidean rhythms
- **Chance** (`chance.py`): Random, weighted choice, shuffling
- **Tonal** (`tonal.py`): Scale degrees, chord progressions
- **Advanced**: Markov chains, L-systems, cellular automata

### Important Implementation Details
- Default timing resolution: 480 PPQN (Pulses Per Quarter Note)
- Patterns use lazy evaluation via Python iterators
- Real-time support through background threads
- Global state management in `globals/` for inter-process sync
- Shorthand notation system in `shorthand/` for quick pattern creation

## Key Design Patterns

### Pattern Class Structure
All patterns follow this structure:
```python
class PPatternName(Pattern):
    abbreviation = "pname"  # For shorthand notation
    
    def __init__(self, ...):
        # Validate inputs
        # Store parameters
        self.reset()
    
    def __next__(self):
        # Return next value or raise StopIteration
    
    def reset(self):
        super().reset()
        # Reset internal state
```

### Common Naming Conventions
- Pattern classes: `P` prefix (e.g., `PSequence`, `PRandom`)
- Test methods: `test_` prefix
- Private methods: `_` prefix
- Constants: `UPPER_SNAKE_CASE`
- Regular methods/variables: `snake_case`

### Error Handling
- Use custom exceptions from `exceptions.py`
- Timeline supports `ignore_exceptions=True` for live coding
- Validate MIDI values (0-127) before output

### Testing Approach
- Use pytest with fixtures
- Test pattern output with `.all()` method
- Verify operator overloading behavior
- Check edge cases (empty sequences, invalid values)

## Development Dependencies
Core dependencies: `python-osc`, `mido`, `python-rtmidi`, `LinkPython-extern`, `numpy`
Test dependencies: `pytest`, `pytest-timeout`, `pytest-runner`

## AI Assistant Integration
This project includes a comprehensive four-part AI assistant configuration:
- **Claude Code**: Deep code analysis via `CLAUDE.md` files
- **Cursor**: Real-time coding guidance (see `.github/copilot-instructions.md`)
- **GitHub Copilot**: Inline suggestions with domain-specific rules
- **OpenAI Codex**: Cloud-based task automation via `AGENTS.md` files

See `AI_SETUP.md` for setup instructions and `ai_ecosystem_summary.md` for overview.
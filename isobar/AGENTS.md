# AGENTS.md - isobar

## Overview
Isobar is a Python library for algorithmic composition and generative music. This directory contains the core library implementation with modular components for pattern generation, event scheduling, and musical output.

## AI Context Integration
This project uses a comprehensive AI ecosystem:
- **CLAUDE.md files**: Deep architectural knowledge and design patterns
- **AGENTS.md files**: Practical execution guidance (this file and subdirectory files)
- **Cursor rules**: `.cursor/rules/` for real-time coding conventions
- **Copilot instructions**: `.github/copilot-instructions.md` for inline suggestions

## Module Structure
Each subdirectory has its own AGENTS.md with specific guidance:

### Core Systems
- `pattern/` - Pattern generation engine (see `pattern/AGENTS.md`)
- `timelines/` - Event scheduling system (see `timelines/AGENTS.md`)
- `io/` - Output device implementations (see `io/AGENTS.md`)

### Support Systems
- `notation/` - String notation parser (see `notation/AGENTS.md`)
- `shorthand/` - Abbreviated syntax (see `shorthand/AGENTS.md`)
- `globals/` - Global state management (see `globals/AGENTS.md`)

### Music Theory
- `note.py` - Note representation and conversion
- `scale.py` - Scale definitions
- `chord.py` - Chord construction
- `key.py` - Key signatures

## Quick Development Commands
```bash
# Install for development
pip install -e .

# Run all tests
pytest

# Run specific module tests
pytest tests/test_pattern*.py
pytest tests/test_timeline*.py

# Quick pattern test
python -c "from isobar import *; print(PSequence([60,64,67]).all())"

# Test with dummy output
python -c "
from isobar import *
from isobar.io.dummy import DummyOutputDevice
t = Timeline(120, output_device=DummyOutputDevice())
t.schedule({'note': PSequence([60,64,67])})
t.run(duration=4)
"
```

## Common Development Tasks

### Creating a new pattern
1. Choose appropriate module (`sequence.py`, `chance.py`, etc.)
2. Follow pattern template in `pattern/CLAUDE.md`
3. Add tests in `tests/test_pattern_*.py`
4. Register abbreviation in `shorthand/abbreviations.py`

### Adding an output device
1. Create directory under `io/`
2. Inherit from `OutputDevice` base class
3. Implement required methods
4. Add device-specific tests

### Debugging issues
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use dummy device to inspect events
from isobar.io.dummy import DummyOutputDevice
# ... use with timeline ...
print(device.events)
```

## Code Navigation
- Pattern implementations: `pattern/*.py`
- Timeline orchestration: `timelines/timeline.py`
- Output devices: `io/*/output.py`
- Tests: `tests/test_*.py`
- Examples: `examples/*.py`

## Validation Checklist
- [ ] All tests pass: `pytest`
- [ ] No linting errors: `flake8 isobar`
- [ ] Patterns have abbreviations
- [ ] MIDI values validated (0-127)
- [ ] Proper cleanup in output devices
- [ ] Documentation updated

## Key Design Principles
1. Patterns are lazy iterators
2. Everything is composable via operators
3. Timeline manages all timing
4. Output devices are pluggable
5. Thread safety for real-time use

## Getting Help
- Architecture questions → Check CLAUDE.md files
- Implementation details → See module-specific AGENTS.md
- Coding conventions → Review Cursor rules
- Quick patterns → Use Copilot suggestions

## Performance Considerations
- Default timing: 480 PPQN
- Use background threads for real-time
- Monitor CPU with many tracks
- Profile with `cProfile` for bottlenecks
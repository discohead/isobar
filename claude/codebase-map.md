# Isobar Codebase Map

## Project Overview
Isobar is a Python library for algorithmic composition, generative music, and sonification. It provides a framework for creating and manipulating musical patterns programmatically, with support for various output devices (MIDI, OSC, SuperCollider, FluidSynth).

## Directory Structure

### Core Library (`isobar/`)
```
isobar/
├── __init__.py          # Package initialization and main exports
├── chord.py             # Chord definitions and operations
├── constants.py         # Global constants (PPQN, tempo, etc.)
├── exceptions.py        # Custom exception classes
├── instrument.py        # Instrument definitions
├── key.py              # Musical key operations
├── note.py             # Note representation and conversions
├── scale.py            # Scale definitions and operations
├── util.py             # Utility functions
│
├── globals/            # Global state management
│   ├── globals.py      # Global parameter sharing
│   └── sync.py         # Process synchronization
│
├── io/                 # Input/Output devices
│   ├── output.py       # Base OutputDevice class
│   ├── cv/             # Control Voltage output
│   ├── dummy/          # Test/debug output
│   ├── fluidsynth/     # FluidSynth integration
│   ├── midi/           # MIDI I/O
│   ├── midifile/       # MIDI file reading/writing
│   ├── mpe/            # MIDI Polyphonic Expression
│   ├── netclock/       # Network clock sync
│   ├── netglobals/     # Network global params
│   ├── osc/            # Open Sound Control
│   ├── signalflow/     # SignalFlow integration
│   ├── socketio/       # Socket.IO support
│   └── supercollider/  # SuperCollider integration
│
├── notation/           # Musical notation parsing
│   └── notation.py     # String notation parser
│
├── pattern/            # Pattern generators (core of isobar)
│   ├── core.py         # Base Pattern class and operators
│   ├── chance.py       # Random/stochastic patterns
│   ├── fade.py         # Fading/interpolation patterns
│   ├── lsystem.py      # L-system patterns
│   ├── markov.py       # Markov chain patterns
│   ├── midi.py         # MIDI-specific patterns
│   ├── monome.py       # Monome grid patterns
│   ├── oscillator.py   # Oscillator patterns
│   ├── scalar.py       # Scalar operations
│   ├── sequence.py     # Sequence patterns
│   ├── static.py       # Static value patterns
│   ├── tonal.py        # Tonal/harmonic patterns
│   └── warp.py         # Time warping patterns
│
├── shorthand/          # Shorthand notation system
│   ├── abbreviations.py # Pattern abbreviations
│   ├── patches.py      # Patch registry
│   ├── setup.py        # Shorthand setup
│   └── sync.py         # Sync utilities
│
└── timelines/          # Event scheduling system
    ├── automation.py   # Parameter automation
    ├── clock.py        # Base clock class
    ├── clock_link.py   # Ableton Link support
    ├── event.py        # Event types
    ├── lfo.py          # LFO modulation
    ├── timeline.py     # Main Timeline class
    └── track.py        # Track scheduling
```

### Examples (`examples/`)
- Basic patterns and sequences (00-07)
- L-system examples (10-11)
- MIDI input/output examples (20-24)
- MIDI file operations (30-32)
- OSC communication (40)
- FluidSynth integration
- SignalFlow integration
- Jupyter notebook example

### Tests (`tests/`)
Comprehensive test coverage for:
- Core functionality (patterns, timelines)
- Music theory components (chord, key, scale)
- I/O operations (MIDI, MIDI files)
- Pattern types and operators
- Timeline components (clock, events, tracks)

### Documentation (`docs/`)
- Getting started guide
- Device documentation
- Event system documentation
- Pattern library reference
- Timeline documentation
- Examples and tutorials

### Auxiliary Scripts (`auxiliary/scripts/`)
- `generate-docs.py` - Generate pattern documentation
- `generate-shorthand-aliases.py` - Generate shorthand mappings

## Key Design Principles

1. **Iterator Protocol**: All patterns implement Python's iterator protocol
2. **Lazy Evaluation**: Patterns generate values on-demand
3. **Operator Overloading**: Patterns support arithmetic operations
4. **Modular I/O**: Clean separation between pattern generation and output
5. **Real-time Support**: Background threading for timing accuracy
6. **High Resolution**: 480 PPQN default for precise timing

## Entry Points

- **Quick Start**: `from isobar import *` imports all commonly used classes
- **Main Classes**: `Timeline`, `Pattern`, various pattern types
- **Common Workflow**: Create patterns → Schedule on timeline → Run timeline
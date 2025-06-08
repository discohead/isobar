# Isobar System Architecture

## Overview

Isobar implements a layered architecture for algorithmic music composition:

```
┌─────────────────────────────────────────────────────────┐
│                    User Code                            │
│         (Patterns, Sequences, Musical Logic)            │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                  Pattern System                         │
│    (Pattern base class, operators, generators)          │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                 Timeline System                         │
│        (Timeline, Track, Clock, Events)                 │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                    I/O Layer                            │
│   (MIDI, OSC, SuperCollider, FluidSynth, etc.)        │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│              External Systems                           │
│     (DAWs, Synthesizers, Audio Software)              │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Pattern System (`isobar.pattern`)

The heart of isobar - implements musical pattern generation through Python's iterator protocol.

**Key Classes:**
- `Pattern`: Abstract base class for all patterns
- `PSequence`: Iterate through a list of values
- `PRandom`: Generate random values
- `PMarkov`: Markov chain generation
- `PLSystem`: L-system pattern generation

**Design Principles:**
- Lazy evaluation via iterators
- Composable through operator overloading
- Stateful but resettable
- Support for infinite sequences

**Pattern Operators:**
```python
# Patterns can be combined mathematically
pattern_sum = pattern1 + pattern2
pattern_product = pattern1 * 2
pattern_modulo = pattern1 % 12
```

### 2. Timeline System (`isobar.timelines`)

Manages temporal scheduling and event dispatch.

**Core Classes:**
- `Timeline`: Main orchestrator, manages tracks and tempo
- `Track`: Schedules pattern-based events
- `Clock`: Provides timing pulses (internal, MIDI, Link)
- `Event`: Base class for musical events

**Event Flow:**
1. Clock generates ticks at specified resolution (default 480 PPQN)
2. Timeline advances and checks each Track
3. Tracks evaluate patterns and generate Events
4. Events are dispatched to OutputDevices
5. OutputDevices translate to external protocols

**Clock Sources:**
- Internal: Software timer-based
- MIDI: External MIDI clock sync
- Link: Ableton Link network sync

### 3. I/O System (`isobar.io`)

Abstracts output to various musical systems.

**Base Class:**
```python
class OutputDevice:
    def note_on(self, note=60, velocity=64, channel=0): pass
    def note_off(self, note=60, channel=0): pass
    def control(self, control=0, value=0, channel=0): pass
    def program_change(self, program=0, channel=0): pass
```

**Implementations:**
- `MidiOutputDevice`: Standard MIDI output
- `OSCOutputDevice`: Open Sound Control messages
- `SuperColliderOutputDevice`: SC language integration
- `FluidSynthOutputDevice`: Built-in synthesis
- `SignalFlowOutputDevice`: Audio synthesis graphs
- `MidiFileOutputDevice`: Write to MIDI files

### 4. Music Theory Components

**Core Classes:**
- `Note`: MIDI note number with string representation
- `Scale`: Scale definitions and operations
- `Chord`: Chord construction and voicing
- `Key`: Key signatures and relationships

**Features:**
- MIDI note ↔ frequency conversion
- Scale degree operations
- Chord inversions and voicings
- Relative key calculations

## Data Flow

### Pattern Evaluation
```
User Pattern Definition
    ↓
Pattern.__next__() called by Track
    ↓
Values processed (may reference other patterns)
    ↓
Scalar value returned
    ↓
Event created with pattern values
```

### Event Scheduling
```
Timeline.run()
    ↓
Clock.tick() generates timing
    ↓
Timeline updates current_time
    ↓
Each Track checks if event due
    ↓
Track evaluates patterns → Event
    ↓
Event queued with timestamp
    ↓
OutputDevice processes event queue
```

## Threading Model

- **Main Thread**: User code, pattern definitions
- **Clock Thread**: Generates timing pulses
- **Timeline Thread**: Processes tracks and events
- **Output Threads**: Per-device event handling

Thread safety achieved through:
- Event queues between threads
- Minimal shared state
- Lock-free where possible

## Extension Points

### Custom Patterns
```python
class PCustom(Pattern):
    def __init__(self, param):
        self.param = param
        self.reset()
    
    def __next__(self):
        # Generate next value
        return computed_value
```

### Custom Output Devices
```python
class CustomOutputDevice(OutputDevice):
    def note_on(self, note, velocity, channel):
        # Convert to target protocol
        self.send_to_device(...)
```

### Custom Clocks
```python
class CustomClock(Clock):
    def run(self):
        while self.running:
            # Generate tick at appropriate time
            self.tick()
```

## Performance Considerations

1. **Timing Resolution**: 480 PPQN ≈ 1ms at 120 BPM
2. **Pattern Evaluation**: Lazy, only when events scheduled
3. **Memory**: Patterns use iterators, not pre-generated lists
4. **Latency Compensation**: Per-device offset available
5. **Clock Multipliers**: Efficient PPQN conversion

## Global State Management

The `globals` module enables:
- Inter-process parameter sharing
- Network synchronization
- Persistent settings

Uses memory-mapped files for IPC efficiency.

## Error Handling Strategy

1. **Pattern Errors**: Caught per-track, track halted
2. **Output Errors**: Logged, timeline continues
3. **Clock Errors**: Fatal, timeline stops
4. **Optional `ignore_exceptions`**: For live coding

## Best Practices

1. **Pattern Design**: Keep patterns simple and composable
2. **Event Scheduling**: Use track-level defaults for common params
3. **Output Selection**: Configure devices before timeline.run()
4. **Timing**: Higher PPQN for tighter timing, lower for efficiency
5. **Memory**: Reset patterns when reusing in long compositions
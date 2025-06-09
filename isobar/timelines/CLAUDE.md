# CLAUDE.md - isobar/timelines

This directory contains the temporal scheduling and event management system that drives isobar's real-time performance.

## Module Overview

The `timelines` module provides the infrastructure for scheduling pattern-generated events in time, managing tempo, synchronizing to external clocks, and dispatching events to output devices. This is where patterns become music.

## Core Components

### timeline.py
- **Purpose**: Main orchestrator for musical time and event scheduling
- **Key Class**: `Timeline`
- **Responsibilities**:
  - Manage global tempo and time
  - Coordinate multiple tracks
  - Route events to output devices
  - Handle start/stop/pause operations
- **Key Methods**:
  - `schedule()`: Add a new track with patterns
  - `run()`: Start timeline execution
  - `stop()`: Stop all playback
  - `background()`: Run in separate thread

### track.py
- **Purpose**: Individual pattern sequences scheduled on timeline
- **Key Class**: `Track`
- **Responsibilities**:
  - Evaluate patterns to generate events
  - Manage track-specific parameters
  - Handle note duration and gate times
  - Support real-time pattern updates
- **Key Features**:
  - Pattern-based scheduling
  - MIDI channel management
  - Note on/off tracking
  - Dynamic pattern updates

### clock.py
- **Purpose**: Abstract base for timing sources
- **Key Classes**:
  - `Clock`: Base clock interface
  - `InternalClock`: Software timer-based
  - `MidiClock`: External MIDI clock sync
- **Timing Resolution**: 480 PPQN (pulses per quarter note) default

### clock_link.py
- **Purpose**: Ableton Link network synchronization
- **Key Class**: `LinkClock`
- **Features**:
  - Network tempo sync
  - Phase alignment
  - Peer discovery
  - Beat-accurate start/stop

### event.py
- **Purpose**: Event types and dispatching
- **Key Classes**:
  - `Event`: Base event class
  - `NoteEvent`: Note on/off events
  - `ControlEvent`: MIDI CC events
  - `ActionEvent`: Arbitrary function calls
- **Event Properties**:
  - Timestamp
  - Target device
  - Event-specific data (note, velocity, etc.)

### automation.py
- **Purpose**: Parameter automation over time
- **Key Features**:
  - Smooth parameter changes
  - Automation curves
  - Pattern-based automation
  - Multi-parameter control

### lfo.py
- **Purpose**: Low-frequency oscillator modulation
- **Key Class**: `LFO`
- **Features**:
  - Multiple waveforms (sine, square, saw, etc.)
  - Phase control
  - Frequency modulation
  - Amplitude scaling

## Event Flow Architecture

```
Clock generates tick
    ↓
Timeline advances time
    ↓
Each Track checked for events
    ↓
Patterns evaluated → Events created
    ↓
Events queued with timestamps
    ↓
OutputDevice processes queue
    ↓
Musical output (MIDI, OSC, etc.)
```

## Key Design Patterns

### Timeline Creation
```python
# Basic timeline
timeline = Timeline(tempo=120)

# With specific output
device = MidiOutputDevice("IAC Driver")
timeline = Timeline(tempo=120, output_device=device)

# With external clock
clock = MidiClock()
timeline = Timeline(clock_source=clock)
```

### Track Scheduling
```python
# Simple track
track = timeline.schedule({
    "note": PSequence([60, 64, 67]),
    "duration": 0.5,
    "velocity": 64
})

# Complex track with patterns
track = timeline.schedule({
    "note": PDegree(PSequence([0, 2, 4, 5]), Scale.major) + 60,
    "duration": PChoice([0.25, 0.5, 1.0]),
    "velocity": PGaussian(64, 10),
    "channel": 0,
    "delay": PSine(0.02, 0, 8)  # Swing
})
```

### Event Types

#### Note Events
```python
timeline.schedule({
    "note": pattern,          # MIDI note number
    "duration": pattern,      # Note length in beats
    "velocity": pattern,      # MIDI velocity (0-127)
    "gate": pattern,         # Note on/off gate (0 or 1)
})
```

#### Control Events
```python
timeline.schedule({
    "control": cc_number,    # MIDI CC number
    "value": pattern,        # CC value (0-127)
    "channel": 0-15
})
```

#### Action Events
```python
def my_function(value):
    print(f"Action triggered: {value}")

timeline.schedule({
    "action": my_function,
    "args": pattern  # Arguments passed to function
})
```

## Implementation Details

### Time Management
```python
# Timeline uses beats as time unit
# 1 beat = 1 quarter note
# Tempo in BPM (beats per minute)

# Time calculation
seconds_per_beat = 60.0 / tempo
ticks_per_second = ticks_per_beat / seconds_per_beat
```

### Track Lifecycle
```python
# Track states
TRACK_PLAYING = "playing"
TRACK_STOPPED = "stopped"
TRACK_FINISHED = "finished"

# Track updates
track.update({
    "note": new_pattern,
    "velocity": new_velocity_pattern
})
```

### Clock Synchronization
```python
# Internal clock
class InternalClock(Clock):
    def run(self):
        while self.running:
            self.tick()
            time.sleep(self.tick_duration)

# External sync
class MidiClock(Clock):
    def handle_midi_clock(self):
        self.tick()  # 24 PPQN MIDI clock
```

## Advanced Features

### Automation
```python
# Automate filter cutoff
automation = timeline.automate({
    "control": 74,  # Filter cutoff
    "target": [0, 127],  # Value range
    "duration": 32,  # Beats
    "curve": "exponential"
})
```

### LFO Modulation
```python
# Add LFO to parameter
lfo = LFO(frequency=0.25, amplitude=20, offset=64)
timeline.schedule({
    "note": pattern,
    "velocity": lfo  # LFO modulates velocity
})
```

### Multi-Output
```python
# Send to multiple devices
midi_out = MidiOutputDevice()
osc_out = OSCOutputDevice("127.0.0.1", 57120)

timeline.schedule({
    "note": pattern,
    "output_device": [midi_out, osc_out]
})
```

## Performance Optimization

1. **Event Queuing**: Pre-calculate events slightly ahead
2. **Thread Pools**: Separate threads for clock, tracks, output
3. **Lock-Free Queues**: Where possible for low latency
4. **Batch Processing**: Group events for efficiency

## Error Handling

### Graceful Degradation
```python
timeline = Timeline(ignore_exceptions=True)  # For live coding

# Exceptions logged but don't stop timeline
# Failed tracks marked as finished
```

### Clock Failure
```python
# Fallback to internal clock if external fails
if not clock.is_running():
    timeline.set_clock(InternalClock())
```

## Testing Timelines

### Unit Tests
```python
def test_timeline_tempo():
    timeline = Timeline(tempo=140)
    assert timeline.tempo == 140
    
def test_track_scheduling():
    timeline = Timeline()
    track = timeline.schedule({"note": PSequence([60])})
    assert len(timeline.tracks) == 1
```

### Integration Tests
```python
def test_event_generation():
    timeline = Timeline(output_device=DummyOutputDevice())
    timeline.schedule({"note": PSequence([60, 64, 67])})
    timeline.run(duration=3)
    # Verify events generated
```

## Best Practices

1. **Start Simple**: Begin with basic patterns, add complexity
2. **Use Background**: Run timeline in background for interactive work
3. **Monitor Performance**: Watch CPU usage with many tracks
4. **Clean Shutdown**: Always call timeline.stop() when done
5. **Error Recovery**: Use ignore_exceptions for live performance

## Related Modules

- `pattern/`: Generates values for timeline events
- `io/`: Output devices that receive events
- `clock.py`: Timing sources
- `constants.py`: Timing constants (PPQN, etc.)
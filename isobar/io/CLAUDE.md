# CLAUDE.md - isobar/io

This directory contains all input/output device implementations for sending and receiving musical events.

## Module Overview

The `io` module provides a pluggable architecture for different output protocols and devices. All output devices inherit from the base `OutputDevice` class and implement a standard interface.

## Base Architecture

### output.py
- **Purpose**: Abstract base class for all output devices
- **Key Interface**:
  ```python
  class OutputDevice:
      def note_on(self, note=60, velocity=64, channel=0): pass
      def note_off(self, note=60, channel=0): pass
      def control(self, control=0, value=0, channel=0): pass
      def program_change(self, program=0, channel=0): pass
      def all_notes_off(self, channel=0): pass
  ```

## Output Device Types

### MIDI (`midi/`)
- **output.py**: Real-time MIDI output via rtmidi
- **input.py**: MIDI input handling for controllers/keyboards
- **Key Features**: Low latency, multi-port support, MIDI clock sync

### MIDI Files (`midifile/`)
- **output.py**: Write patterns to standard MIDI files
- **input.py**: Read and parse MIDI files into patterns
- **Key Features**: SMF format 0/1 support, tempo maps, multi-track

### OSC (`osc/`)
- **output.py**: Open Sound Control protocol implementation
- **Key Features**: Network messaging, flexible addressing, bundle support

### SuperCollider (`supercollider/`)
- **output.py**: Direct integration with SuperCollider synthesis
- **Key Features**: sclang communication, SynthDef support, real-time control

### FluidSynth (`fluidsynth/`)
- **output.py**: Built-in software synthesis via FluidSynth
- **Key Features**: SoundFont support, multi-channel, effects processing

### SignalFlow (`signalflow/`)
- **output.py**: Integration with SignalFlow audio graphs
- **Key Features**: Modular synthesis, parameter automation, trigger events

### MPE (`mpe/`)
- **output.py**: MIDI Polyphonic Expression support
- **note.py**: MPE note management
- **Key Features**: Per-note expression, pitch bend, pressure

### Network (`netclock/`, `netglobals/`)
- **netclock/**: Network-based clock synchronization
- **netglobals/**: Distributed global parameter sharing
- **Key Features**: Multi-client sync, low latency protocols

### Other Devices
- **cv/**: Control Voltage output for modular synths
- **socketio/**: WebSocket-based communication
- **dummy/**: Testing and debugging output

## Key Design Patterns

### Device Selection
```python
# Automatic default device
timeline = Timeline(120)  # Uses system default MIDI

# Explicit device
device = MidiOutputDevice("IAC Driver Bus 1")
timeline = Timeline(120, output_device=device)
```

### Multi-Device Output
```python
# Send to multiple devices
midi_out = MidiOutputDevice()
osc_out = OSCOutputDevice("127.0.0.1", 57120)

timeline.schedule({
    "note": pattern,
    "output_device": [midi_out, osc_out]
})
```

### Device-Specific Parameters
```python
# MPE example
timeline.schedule({
    "note": pattern,
    "pressure": PLinear(0, 127, 16),
    "pitch_bend": PSine(0, 0.5, 8),
    "output_device": MPEOutputDevice()
})
```

## Implementation Guidelines

1. **Validation**: Always validate MIDI values (0-127)
2. **Threading**: Handle output in separate threads for timing
3. **Buffering**: Use appropriate buffer sizes for latency/stability
4. **Error Handling**: Gracefully handle device disconnection
5. **Cleanup**: Properly close devices and free resources

## Common Patterns

### MIDI Value Validation
```python
note = int(note) % 128
velocity = int(velocity) % 128
channel = int(channel) % 16
```

### Device Initialization
```python
def __init__(self, port_name=None):
    super().__init__()
    self.midi_out = rtmidi.MidiOut()
    if port_name:
        self.open(port_name)
```

### Event Queuing
```python
def note_on(self, note, velocity, channel):
    message = [0x90 | channel, note, velocity]
    self.send(message)
```

## Testing Output Devices

```python
# Test with dummy device
dummy = DummyOutputDevice()
timeline = Timeline(120, output_device=dummy)
timeline.schedule({"note": PSequence([60, 64, 67])})
timeline.run(duration=4)
print(dummy.events)  # Inspect generated events
```

## Performance Considerations

- Use buffered output for file-based devices
- Minimize latency for real-time devices
- Consider device-specific timing compensation
- Handle clock drift in networked scenarios

## Related Modules

- `timelines/`: Event scheduling and dispatch
- `pattern/`: Pattern generation for events
- `constants.py`: MIDI constants and defaults
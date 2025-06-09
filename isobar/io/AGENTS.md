# AGENTS.md - isobar/io

## Module Overview
Input/output device implementations for musical events. All devices inherit from `OutputDevice` base class and implement standard interface for MIDI, OSC, SuperCollider, etc.

## AI Context Integration
- **Deep context**: See `CLAUDE.md` in this directory for architecture
- **Implementation patterns**: Check `.cursor/rules/components/io-devices.mdc`
- **Device templates**: See `.github/instructions/output-device.instructions.md`

## Key Files
- `output.py` - Base `OutputDevice` class
- `midi/output.py` - Real-time MIDI via rtmidi
- `osc/output.py` - OSC protocol implementation
- `midifile/output.py` - MIDI file writer
- `dummy/output.py` - Testing device

## Development Commands
```bash
# Run all I/O tests
pytest tests/test_io_*.py -v

# Test MIDI devices (requires rtmidi)
python -m pytest tests/test_io_midi.py

# List available MIDI ports
python -c "import rtmidi; print(rtmidi.MidiOut().get_ports())"

# Test with dummy device
python examples/test_output_device.py
```

## Testing Instructions

### Adding a new output device
1. Create new directory under `io/`
2. Inherit from `OutputDevice` in `output.py`
3. Implement required methods: `note_on()`, `note_off()`, `control()`
4. Add device-specific parameters if needed
5. Create tests in `tests/test_io_yourdevice.py`
6. Update `__init__.py` exports

### Testing device implementation
```python
# Use dummy device for testing
from isobar.io.dummy import DummyOutputDevice
device = DummyOutputDevice()
timeline = Timeline(120, output_device=device)
# ... schedule patterns ...
timeline.run(duration=4)
print(device.events)  # Inspect generated events
```

## Common Tasks

### MIDI value validation
All MIDI devices must validate:
- Notes: 0-127
- Velocity: 0-127  
- Channels: 0-15
- CC values: 0-127

### Device initialization pattern
```python
def __init__(self, port_name=None):
    super().__init__()
    self.setup_device()
    if port_name:
        self.open(port_name)
```

## Code Pointers
- Base interface: `OutputDevice` class in `output.py`
- MIDI implementation: `MidiOutputDevice` in `midi/output.py`
- Event validation: Look for `% 128` and `% 16` patterns
- Threading: Check `_output_thread` methods

## Validation Steps
1. Run device-specific tests
2. Verify MIDI values are clamped (0-127)
3. Test device cleanup on `close()`
4. Check thread termination
5. Verify no resource leaks with long runs

## Debugging Tips
- Use `DummyOutputDevice` to inspect event stream
- Enable debug logging: `logging.getLogger('isobar.io').setLevel(logging.DEBUG)`
- Monitor MIDI with external tools (MIDI Monitor on macOS)
- Check device cleanup in `__exit__` methods
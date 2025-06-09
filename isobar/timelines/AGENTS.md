# AGENTS.md - isobar/timelines

## Module Overview
Temporal scheduling and event management system. Manages timing, tracks, clocks, and event dispatch to output devices.

## AI Context Integration
- **Architecture details**: See `CLAUDE.md` in this directory
- **Timeline patterns**: Check `.cursor/rules/components/timelines.mdc`
- **Event handling**: See `.github/instructions/event-scheduling.md`
- **Live coding**: See `claude/workflows/live-coding.md`

## Key Files
- `timeline.py` - Main `Timeline` class
- `track.py` - `Track` pattern scheduling
- `clock.py` - Clock sources (internal, MIDI, Link)
- `event.py` - Event types (Note, Control, Action)
- `automation.py` - Parameter automation
- `lfo.py` - LFO modulation

## Development Commands
```bash
# Run timeline tests
pytest tests/test_timeline*.py -v

# Test with dummy output
python -c "
from isobar import *
from isobar.io.dummy import DummyOutputDevice
t = Timeline(120, output_device=DummyOutputDevice())
t.schedule({'note': PSequence([60,64,67])})
t.run(duration=4)
"

# Test clock sync
python examples/21.ex-midi-clock-sync-in.py

# Monitor timeline events
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# ... timeline code ...
"
```

## Common Timeline Tasks

### Basic scheduling
```python
timeline = Timeline(tempo=120)

# Simple track
track = timeline.schedule({
    "note": PSequence([60, 64, 67]),
    "duration": 0.5,
    "velocity": 64
})

timeline.run()
```

### Live coding setup
```python
# IMPORTANT: Use ignore_exceptions for stability
timeline = Timeline(120, ignore_exceptions=True)
timeline.start()  # Run in background

# Add/modify tracks on the fly
bass = timeline.schedule({"note": seq([36, 41])})
bass.update({"note": seq([36, 39, 41])})  # Change pattern
bass.stop()  # Mute track
```

### Multi-device output
```python
midi = MidiOutputDevice()
osc = OSCOutputDevice("127.0.0.1", 57120)

timeline.schedule({
    "note": pattern,
    "output_device": [midi, osc]
})
```

## Clock Configuration

### Internal clock (default)
```python
timeline = Timeline(tempo=120)  # Software timer
```

### MIDI clock sync
```python
from isobar.timelines.clock import MidiClock
clock = MidiClock(midi_in)
timeline = Timeline(clock_source=clock)
```

### Ableton Link
```python
from isobar.timelines.clock_link import LinkClock
clock = LinkClock()
timeline = Timeline(clock_source=clock)
```

## Code Pointers
- Timeline main loop: `Timeline._run()` in `timeline.py`
- Track scheduling: `Track.update()` in `track.py`
- Event dispatch: `Timeline._process_event()` in `timeline.py`
- Clock interface: `Clock` base class in `clock.py`
- Note tracking: `Track._note_offs` dict

## Testing & Debugging

### Test event generation
```python
from isobar.io.dummy import DummyOutputDevice

device = DummyOutputDevice()
timeline = Timeline(120, output_device=device)
timeline.schedule({"note": PSequence([60, 64, 67])})
timeline.run(duration=4)

# Inspect events
for event in device.events:
    print(f"{event.type}: {event.data}")
```

### Debug timing issues
```python
# Enable debug logging
import logging
logging.getLogger('isobar.timelines').setLevel(logging.DEBUG)

# Monitor tick accuracy
timeline.debug_timing = True
```

## Validation Steps
1. Run `pytest tests/test_timeline.py`
2. Verify proper note-off generation
3. Test clock sync accuracy
4. Check thread cleanup on stop
5. Validate event ordering
6. Test `ignore_exceptions` mode

## Performance Tips
- Use `ignore_exceptions=True` for live coding
- Run timeline in background for interactive work
- Monitor CPU with many tracks
- Pre-calculate complex patterns
- Use appropriate PPQN for timing needs

## Common Issues
- Missing note-offs (check duration/gate)
- Clock drift with external sync
- Thread cleanup on timeline.stop()
- Event timing with high CPU load
- Pattern exceptions stopping timeline

## Event Types Reference
```python
# Note events
{"note": 60, "duration": 1, "velocity": 64}

# Control events  
{"control": 7, "value": 100, "channel": 0}

# Action events
{"action": my_function, "args": [1, 2, 3]}

# Pattern parameters
{"note": seq([60,64,67]), "duration": ch([0.25, 0.5])}
```
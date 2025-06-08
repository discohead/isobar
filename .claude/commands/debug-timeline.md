# Debug Timeline Issues

<task>
Debug and diagnose issues with Timeline scheduling and event processing.
</task>

<common_issues>
1. **Events not playing**: Check output device, channel, patterns
2. **Timing problems**: Verify clock source, PPQN settings
3. **Pattern errors**: Use ignore_exceptions or check pattern output
4. **Track limit**: Check max_tracks setting
5. **MIDI issues**: Verify MIDI device connection
</common_issues>

<debugging_steps>
## 1. Enable Detailed Logging
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
```

## 2. Check Timeline State
```python
# Inspect timeline
print(f"Running: {timeline.running}")
print(f"Current time: {timeline.current_time}")
print(f"Tempo: {timeline.tempo}")
print(f"Tracks: {len(timeline.tracks)}")
print(f"Output devices: {timeline.output_devices}")
```

## 3. Verify Pattern Output
```python
# Test pattern in isolation
pattern = YourPattern()
print(f"First 10 values: {pattern.all(10)}")

# Check for StopIteration
try:
    for i in range(20):
        print(f"{i}: {next(pattern)}")
except StopIteration:
    print(f"Pattern stopped at index {i}")
```

## 4. Monitor Events
```python
# Create a debug output device
class DebugOutput(OutputDevice):
    def note_on(self, note, velocity, channel):
        print(f"[NOTE ON] note={note} vel={velocity} ch={channel}")
    
    def note_off(self, note, channel):
        print(f"[NOTE OFF] note={note} ch={channel}")
    
    def control(self, control, value, channel):
        print(f"[CONTROL] cc={control} val={value} ch={channel}")

# Use it
debug_device = DebugOutput()
timeline = Timeline(output_device=debug_device)
```

## 5. Track Individual Tracks
```python
# Add track with reference
track = timeline.schedule({
    "note": PSequence([60, 64, 67]),
    "duration": 1
})

print(f"Track playing: {track.playing}")
print(f"Track current time: {track.current_time}")
print(f"Track events: {track.events}")
```

## 6. Clock Diagnostics
```python
# Check clock behavior
class ClockDebugger:
    def __init__(self, timeline):
        self.timeline = timeline
        self.tick_count = 0
        self.last_time = time.time()
    
    def monitor(self, duration=5):
        start_time = time.time()
        start_beats = self.timeline.current_time
        
        time.sleep(duration)
        
        end_time = time.time()
        end_beats = self.timeline.current_time
        
        elapsed_time = end_time - start_time
        elapsed_beats = end_beats - start_beats
        
        print(f"Elapsed time: {elapsed_time:.2f}s")
        print(f"Elapsed beats: {elapsed_beats:.2f}")
        print(f"Effective BPM: {(elapsed_beats / elapsed_time) * 60:.1f}")

# Use it
debugger = ClockDebugger(timeline)
debugger.monitor(5)
```

## 7. MIDI-Specific Debugging
```python
# List available MIDI devices
import mido
print("MIDI Outputs:", mido.get_output_names())
print("MIDI Inputs:", mido.get_input_names())

# Test MIDI output directly
output = mido.open_output()
output.send(mido.Message('note_on', note=60, velocity=64))
time.sleep(1)
output.send(mido.Message('note_off', note=60))
```

## 8. Pattern State Inspection
```python
def inspect_pattern(pattern, name="Pattern"):
    """Deep inspection of pattern state."""
    print(f"\n=== {name} ===")
    print(f"Type: {type(pattern).__name__}")
    print(f"Repr: {repr(pattern)}")
    
    # Get attributes
    attrs = {k: v for k, v in vars(pattern).items() if not k.startswith('_')}
    for key, value in attrs.items():
        print(f"{key}: {value}")
    
    # Test iteration
    try:
        pattern.reset()
        values = pattern.all(10)
        print(f"First 10 values: {values}")
    except Exception as e:
        print(f"Error getting values: {e}")

# Use it
inspect_pattern(my_pattern, "My Pattern")
```

## 9. Timeline Event Queue
```python
# Monitor event scheduling
original_tick = timeline._tick

def debug_tick(self):
    print(f"[TICK] Time: {self.current_time:.3f}")
    for i, track in enumerate(self.tracks):
        if track.playing:
            print(f"  Track {i}: next_event_time={track.next_event_time:.3f}")
    original_tick()

timeline._tick = debug_tick.__get__(timeline, Timeline)
```

## 10. Error Traceback
```python
# Run with full traceback
timeline = Timeline(ignore_exceptions=False)
try:
    timeline.schedule({
        "note": problematic_pattern,
        "duration": 1
    })
    timeline.run()
except Exception as e:
    import traceback
    traceback.print_exc()
```
</debugging_steps>

<pattern_specific_checks>
```python
# Check for common pattern issues

# 1. Infinite patterns that should be finite
p = YourPattern()
if len(list(itertools.islice(p, 1000))) == 1000:
    print("Warning: Pattern might be infinite")

# 2. Patterns returning non-numeric values
values = p.all(10)
non_numeric = [v for v in values if not isinstance(v, (int, float))]
if non_numeric:
    print(f"Non-numeric values: {non_numeric}")

# 3. Patterns returning out-of-range MIDI values
invalid_notes = [v for v in values if not 0 <= v <= 127]
if invalid_notes:
    print(f"Invalid MIDI values: {invalid_notes}")
```
</pattern_specific_checks>

<performance_monitoring>
```python
import cProfile
import pstats

# Profile timeline execution
profiler = cProfile.Profile()
profiler.enable()

timeline.run(duration=10)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```
</performance_monitoring>
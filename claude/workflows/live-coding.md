# Workflow: Live Coding with Isobar

## Setup for Live Coding

### 1. Create a Persistent Timeline
```python
from isobar import *
import logging

# Set up logging for feedback
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

# Create timeline with ignore_exceptions for stability
timeline = Timeline(tempo=120, ignore_exceptions=True)
timeline.start()  # Run in background
```

### 2. Use Track References
```python
# Keep track references for manipulation
bass_track = None
lead_track = None
drums_track = None
```

## Live Pattern Manipulation

### Adding Tracks On-the-Fly
```python
# Start a bass line
bass_track = timeline.schedule({
    "note": PSequence([36, 36, 41, 43]),
    "duration": 1,
    "velocity": 80,
    "channel": 1
})

# Add a lead melody
lead_track = timeline.schedule({
    "note": PChoice([60, 63, 65, 67, 70, 72]) + PRandom(0, 12),
    "duration": PChoice([0.25, 0.5]),
    "velocity": PGaussian(64, 10),
    "channel": 0
})
```

### Modifying Running Patterns
```python
# Change the bass pattern
if bass_track:
    bass_track.update({
        "note": PSequence([36, 38, 41, 46])  # New progression
    })

# Add effects to lead
if lead_track:
    lead_track.update({
        "delay": PSine(0.1, 0, 4),  # Add swing
        "control": {7: PLinear(64, 127, 8)}  # Volume fade
    })
```

### Stopping and Restarting Tracks
```python
# Mute the lead
if lead_track:
    lead_track.stop()

# Restart with variation
lead_track = timeline.schedule({
    "note": PChoice([72, 75, 77, 79]) + PRandom(-12, 0),
    "duration": 0.125,  # Faster notes
    "velocity": 80
})
```

## Pattern Development Techniques

### 1. Gradual Evolution
```python
# Start simple
pattern = PSequence([60, 64, 67])

# Add complexity over time
pattern = PChoice([60, 64, 67])
pattern = PChoice([60, 64, 67]) + PBrown(0, 12, 1)
pattern = PChoice([60, 64, 67]) + PBrown(0, 24, 2)
```

### 2. Layer Building
```python
# Layer 1: Rhythm
kick = timeline.schedule({
    "note": 36,
    "duration": 1,
    "gate": PBjorklund(3, 8)
})

# Layer 2: Bass
bass = timeline.schedule({
    "note": PSequence([36, 39, 41, 34]),
    "duration": 0.5,
    "velocity": 70,
    "channel": 1
})

# Layer 3: Chords
chords = timeline.schedule({
    "note": PSequence([[60, 64, 67], [58, 62, 65], [57, 60, 64], [55, 59, 62]]),
    "duration": 2,
    "channel": 2
})
```

### 3. Parameter Animation
```python
# Animate filter cutoff
filter_track = timeline.schedule({
    "control": 74,  # Filter cutoff CC
    "value": PSine(64, 32, 16) + PBrown(0, 16, 2),
    "channel": 0
})

# Modulate resonance
res_track = timeline.schedule({
    "control": 71,  # Resonance CC
    "value": PInterpolate(0, 100, 32),
    "channel": 0
})
```

## Live Coding Patterns Library

### Rhythmic Generators
```python
# Evolving drum pattern
class PEvolvingDrums(Pattern):
    def __init__(self):
        self.density = 4
        self.reset()
    
    def __next__(self):
        # Increase density over time
        if random.random() < 0.01:
            self.density = min(16, self.density + 1)
        
        pattern = PBjorklund(self.density, 16)
        return next(pattern)

# Use it
drums = timeline.schedule({
    "note": 36,
    "gate": PEvolvingDrums(),
    "duration": 0.25
})
```

### Harmonic Progressions
```python
# Jazz chord progression generator
progressions = {
    "ii-V-I": [[2, 5, 9], [5, 9, 0], [0, 4, 7]],
    "I-vi-ii-V": [[0, 4, 7], [9, 0, 4], [2, 5, 9], [5, 9, 0]],
    "blues": [[0, 4, 7], [0, 4, 7], [0, 4, 7], [0, 4, 7],
              [5, 9, 0], [5, 9, 0], [0, 4, 7], [0, 4, 7],
              [7, 11, 2], [5, 9, 0], [0, 4, 7], [0, 4, 7]]
}

# Play progression
progression = timeline.schedule({
    "note": PSequence(progressions["ii-V-I"]) + 60,
    "duration": 2,
    "channel": 3
})
```

### Melodic Generators
```python
# Call and response pattern
call = PSequence([67, 69, 67, 65, 64])
response = PChoice([60, 62, 64]) + PRandom(0, 12)

melody = timeline.schedule({
    "note": PConcat([call, response]),
    "duration": PChoice([0.25, 0.5, 0.5, 1]),
    "velocity": PSequence([80, 60, 60, 70])
})
```

## Performance Control

### Tempo Changes
```python
# Gradual tempo change
timeline.tempo = 120
for i in range(60):
    timeline.tempo += 1
    time.sleep(0.5)

# Sudden tempo shifts
timeline.tempo = 140  # Jump to 140 BPM
```

### Dynamic Muting
```python
# Create mute groups
drum_tracks = []
melodic_tracks = []

# Add to groups when creating
drum_tracks.append(kick_track)
melodic_tracks.append(lead_track)

# Mute/unmute groups
def mute_drums():
    for track in drum_tracks:
        track.stop()

def unmute_drums():
    for track in drum_tracks:
        track.start()
```

### Section Management
```python
# Define sections
def verse():
    # Stop all tracks
    timeline.stop_all_tracks()
    
    # Start verse patterns
    timeline.schedule({...})  # Bass
    timeline.schedule({...})  # Drums

def chorus():
    timeline.stop_all_tracks()
    
    # Bigger arrangement
    timeline.schedule({...})  # Full drums
    timeline.schedule({...})  # Bass
    timeline.schedule({...})  # Lead
    timeline.schedule({...})  # Pads

# Switch sections
verse()
# ... perform for a while ...
chorus()
```

## Error Recovery

### Safe Pattern Updates
```python
def safe_update(track, params):
    """Update track with error handling"""
    try:
        if track and track.playing:
            track.update(params)
        else:
            print("Track not playing")
    except Exception as e:
        print(f"Update failed: {e}")
```

### Pattern Validation
```python
def validate_pattern(pattern, length=32):
    """Test pattern before using"""
    try:
        values = pattern.all(length)
        return all(0 <= v <= 127 for v in values if isinstance(v, (int, float)))
    except:
        return False

# Use it
new_pattern = PChoice([60, 64, 67]) + PBrown(0, 24)
if validate_pattern(new_pattern):
    track.update({"note": new_pattern})
```

## Quick Tips

1. **Use Jupyter/IPython**: Better for interactive coding
2. **Keep timeline running**: Use `ignore_exceptions=True`
3. **Name your tracks**: Easy to reference later
4. **Build incrementally**: Start simple, add complexity
5. **Use helper functions**: For common operations
6. **Monitor logs**: See what's happening in real-time
7. **Have a kill switch**: `timeline.stop()` ready

## Example Live Set Structure
```python
# Initialize
timeline = Timeline(120, ignore_exceptions=True)
timeline.start()

# Build up
drums = add_drums()
time.sleep(8)  # 8 beats

bass = add_bass() 
time.sleep(8)

lead = add_lead()
time.sleep(16)

# Break down
lead.stop()
time.sleep(4)

drums.stop()
time.sleep(4)

# Build again with variation
drums = add_drums_variation()
bass.update({"note": new_bass_pattern})
lead = add_lead_variation()
```
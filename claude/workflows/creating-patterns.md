# Workflow: Creating Musical Patterns

## Basic Pattern Creation

### 1. Simple Sequence
```python
from isobar import *

# Create a simple melodic sequence
melody = PSequence([60, 62, 64, 65, 67, 69, 71, 72])

# Play it twice
melody_twice = PSequence([60, 62, 64, 65, 67, 69, 71, 72], repeats=2)
```

### 2. Using Pattern Arithmetic
```python
# Transpose the melody up an octave
melody_high = melody + 12

# Create harmony by stacking thirds
harmony = melody + [0, 4, 7]  # Creates chords

# Random velocity variations
velocity = PRandom(40, 80)
```

### 3. Rhythmic Patterns
```python
# Euclidean rhythm: 5 hits over 8 steps
rhythm = PEuclidean(5, 8)

# Map to note durations
durations = PMap(rhythm, {1: 0.5, 0: 0})  # Hits = eighth notes, rests = silence
```

## Advanced Pattern Techniques

### 1. Stochastic Patterns
```python
# Weighted random choice
notes = PChoice([60, 64, 67, 72], weights=[4, 2, 2, 1])

# Brownian motion
wandering = PBrown(0, 127, step=2)

# Markov chain
markov = PMarkov({
    60: {62: 0.5, 64: 0.3, 67: 0.2},
    62: {60: 0.3, 64: 0.4, 65: 0.3},
    64: {62: 0.3, 65: 0.3, 67: 0.4},
    65: {64: 0.5, 67: 0.5},
    67: {65: 0.3, 69: 0.7},
    69: {67: 1.0}
})
```

### 2. Pattern Transformation
```python
# Skip every other note
sparse = PSkip(melody, 2)

# Reverse the pattern
backwards = PReverse(melody)

# Stutter/repeat each value
stuttered = PStutter(melody, 2)

# Subpatterns
variation = PSubsequence(melody, PSequence([0, 2, 4, 5]))
```

### 3. Time-Based Patterns
```python
# Linear interpolation
fade_in = PInterpolate(0, 127, steps=16)

# LFO-style oscillation
lfo = PSine(period=4, amplitude=12, offset=64)

# Accelerando/ritardando
tempo_change = PLinear(120, 180, time=32)  # Speed up over 32 beats
```

## Pattern Composition Workflow

### Step 1: Define Core Elements
```python
# Melodic material
motif = PSequence([0, 2, 5, 7, 5, 2])
bass_line = PSequence([0, 0, -5, -3])

# Rhythmic material
pulse = PSequence([1, 1, 1, 1])
syncopation = PSequence([1, 0, 1, 1, 0, 1, 1, 0])
```

### Step 2: Transform and Develop
```python
# Create variations
motif_inverted = 12 - motif  # Inversion
motif_transposed = motif + PSeries(0, 1)  # Rising sequence

# Combine rhythms
composite_rhythm = pulse * syncopation  # Rhythmic and
```

### Step 3: Structure the Composition
```python
# A-B-A form
structure = PConcat([
    motif * 4,           # A section
    motif_inverted * 2,  # B section  
    motif * 4            # A return
])

# Add dynamics
dynamics = PConcat([
    PSequence([64] * 16),  # mf
    PLinear(64, 80, 8),    # crescendo
    PSequence([80] * 8),   # f
    PLinear(80, 48, 8)     # diminuendo
])
```

## Pattern Scheduling Workflow

### Step 1: Create Timeline
```python
timeline = Timeline(tempo=120)
```

### Step 2: Schedule Pattern Events
```python
# Basic note scheduling
timeline.schedule({
    "note": melody,
    "duration": 0.5,
    "velocity": 64
})

# Multiple tracks
timeline.schedule({
    "note": bass_line,
    "duration": 1,
    "velocity": 80,
    "channel": 1
})
```

### Step 3: Advanced Scheduling
```python
# With pattern-based parameters
timeline.schedule({
    "note": motif + 60,  # Middle C base
    "duration": PChoice([0.25, 0.5, 1]),
    "velocity": PGaussian(64, 10),
    "delay": PSine(0.1, 0, 8)  # Slight timing variations
})

# Control changes
timeline.schedule({
    "control": 7,  # Volume CC
    "value": PLinear(0, 127, 32),
    "channel": 0
})
```

### Step 4: Run Timeline
```python
# Run until stopped
timeline.run()

# Or run for specific duration
timeline.run(duration=32)  # 32 beats
```

## Common Pattern Recipes

### Arpeggiator
```python
chord = [60, 64, 67, 72]
arp = PCycle(chord)
arp_pattern = PArpeggiator(chord, type="up-down")
```

### Drum Pattern
```python
kick = PBjorklund(4, 16)  # 4 kicks in 16 steps
snare = PSequence([0, 0, 0, 0, 1, 0, 0, 0] * 2)
hihat = PBjorklund(13, 16)  # Complex hihat pattern

timeline.schedule({"note": 36, "duration": 0.25, "gate": kick})
timeline.schedule({"note": 38, "duration": 0.25, "gate": snare})
timeline.schedule({"note": 42, "duration": 0.25, "gate": hihat, "velocity": PRandom(40, 60)})
```

### Generative Melody
```python
# Define a scale
scale = Scale.major

# Random walk within scale
melody = PWalk(
    start=0,
    step=PChoice([-2, -1, 0, 1, 2], weights=[1, 3, 1, 3, 1]),
    min=0,
    max=14  # Two octaves
)

# Map to actual notes
notes = PMap(melody, lambda x: scale[x] + 60)
```

## Debugging Patterns

### Inspect Pattern Output
```python
# Get first N values
print(pattern.all(16))

# Step through manually
pattern.reset()
for i in range(10):
    print(next(pattern))
```

### Test in Isolation
```python
# Test without timeline
p = YourComplexPattern()
values = p.all(32)
assert all(0 <= v <= 127 for v in values)  # Valid MIDI notes
```

### Visualize Pattern
```python
import matplotlib.pyplot as plt

values = pattern.all(64)
plt.plot(values)
plt.show()
```
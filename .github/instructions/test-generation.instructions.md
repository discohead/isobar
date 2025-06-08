# Test Generation Instructions

Generate tests following these patterns:

## Basic Test Structure
```python
import pytest
import isobar as iso

def test_pattern_basic():
    """Test basic functionality."""
    p = iso.PPattern(param)
    
    # Test single values
    assert next(p) == expected_first
    assert next(p) == expected_second
    
    # Test sequence
    p.reset()
    assert p.all(4) == [val1, val2, val3, val4]

def test_pattern_reset():
    """Test reset behavior."""
    p = iso.PPattern(param)
    next(p)
    next(p)
    p.reset()
    assert next(p) == first_value

def test_pattern_operators():
    """Test arithmetic operators."""
    p = iso.PPattern(param)
    
    # Addition
    p2 = p + 10
    assert next(p2) == expected + 10
    
    # Multiplication
    p3 = p * 2
    assert next(p3) == expected * 2

def test_pattern_stopiteration():
    """Test finite patterns."""
    p = iso.PPattern(param, repeats=1)
    values = p.all()  # Exhaust pattern
    
    with pytest.raises(StopIteration):
        next(p)

def test_pattern_edge_cases():
    """Test error conditions."""
    # Invalid input
    with pytest.raises(ValueError):
        iso.PPattern(invalid_param)
    
    # Empty sequence
    p = iso.PPattern([])
    with pytest.raises(StopIteration):
        next(p)
```

## Mock External Resources
```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_midi_output():
    with patch('mido.open_output') as mock:
        yield mock

def test_midi_device(mock_midi_output):
    device = iso.MidiOutputDevice()
    device.note_on(60, 100, 0)
    
    # Verify MIDI message sent
    mock_midi_output.return_value.send.assert_called()
```

## Timeline Testing
```python
def test_timeline_integration():
    """Test pattern in timeline context."""
    timeline = iso.Timeline(tempo=480)  # Fast tempo
    
    events = []
    timeline.schedule({
        "note": iso.PPattern(param),
        "duration": 0.1,
        "action": lambda: events.append(1)
    })
    
    timeline.run(duration=1)
    assert len(events) == expected_count
```
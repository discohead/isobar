# Add New Output Device

<task>
Create a new output device implementation for isobar.
</task>

<context>
Output devices in isobar translate pattern events into external protocols (MIDI, OSC, etc).
All output devices inherit from the OutputDevice base class and implement a standard interface.
</context>

<template>
```python
import logging
from ..output import OutputDevice

log = logging.getLogger(__name__)

class YourOutputDevice(OutputDevice):
    """
    Output device for [protocol/system name].
    
    This device sends events to [destination description].
    
    Args:
        param1: Description of connection parameter
        param2: Optional configuration parameter
        
    Examples:
        >>> device = YourOutputDevice("connection_string")
        >>> timeline = Timeline(output_device=device)
    """
    
    def __init__(self, param1, param2=None):
        super().__init__()
        
        self.param1 = param1
        self.param2 = param2
        
        # Initialize connection
        self.connection = None
        self._connect()
        
        # Device-specific timing if different from default
        self._ticks_per_beat = 24  # e.g., MIDI clock
        
        log.info(f"Initialized {self.__class__.__name__}")
    
    def _connect(self):
        """Establish connection to external system."""
        try:
            # Your connection logic
            self.connection = create_connection(self.param1)
            log.info(f"Connected to {self.param1}")
        except Exception as e:
            log.error(f"Failed to connect: {e}")
            raise
    
    @property
    def ticks_per_beat(self):
        """Return device-specific timing resolution."""
        return self._ticks_per_beat
    
    def tick(self):
        """
        Called on each timeline tick.
        Use for devices that need clock sync.
        """
        if self.connection:
            # Send timing/clock message
            self.connection.send_clock()
    
    def start(self):
        """Called when timeline starts."""
        if self.connection:
            # Send start message
            self.connection.send_start()
            log.debug("Sent start message")
    
    def stop(self):
        """Called when timeline stops."""
        if self.connection:
            # Send stop message
            self.connection.send_stop()
            # Clean up
            self.all_notes_off()
            log.debug("Sent stop message")
    
    def note_on(self, note=60, velocity=64, channel=0):
        """
        Send note on event.
        
        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)
            channel: Channel number (0-15)
        """
        if not self.connection:
            return
            
        # Validate inputs
        note = int(note) % 128
        velocity = int(velocity) % 128
        channel = int(channel) % 16
        
        # Convert to your protocol format
        message = self._format_note_on(note, velocity, channel)
        self.connection.send(message)
        
        log.debug(f"Note on: {note} vel={velocity} ch={channel}")
    
    def note_off(self, note=60, channel=0):
        """
        Send note off event.
        
        Args:
            note: MIDI note number (0-127)
            channel: Channel number (0-15)
        """
        if not self.connection:
            return
            
        note = int(note) % 128
        channel = int(channel) % 16
        
        message = self._format_note_off(note, channel)
        self.connection.send(message)
        
        log.debug(f"Note off: {note} ch={channel}")
    
    def control(self, control=0, value=0, channel=0):
        """
        Send control change event.
        
        Args:
            control: Control number (0-127)
            value: Control value (0-127)
            channel: Channel number (0-15)
        """
        if not self.connection:
            return
            
        control = int(control) % 128
        value = int(value) % 128
        channel = int(channel) % 16
        
        message = self._format_control(control, value, channel)
        self.connection.send(message)
        
        log.debug(f"Control: {control}={value} ch={channel}")
    
    def program_change(self, program=0, channel=0):
        """
        Send program change event.
        
        Args:
            program: Program number (0-127)
            channel: Channel number (0-15)
        """
        if not self.connection:
            return
            
        program = int(program) % 128
        channel = int(channel) % 16
        
        message = self._format_program_change(program, channel)
        self.connection.send(message)
        
        log.debug(f"Program change: {program} ch={channel}")
    
    def _format_note_on(self, note, velocity, channel):
        """Format note on for your protocol."""
        # Protocol-specific formatting
        return {"type": "note_on", "note": note, "velocity": velocity, "channel": channel}
    
    def _format_note_off(self, note, channel):
        """Format note off for your protocol."""
        return {"type": "note_off", "note": note, "channel": channel}
    
    def _format_control(self, control, value, channel):
        """Format control change for your protocol."""
        return {"type": "control", "control": control, "value": value, "channel": channel}
    
    def _format_program_change(self, program, channel):
        """Format program change for your protocol."""
        return {"type": "program", "program": program, "channel": channel}
    
    def __del__(self):
        """Clean up connection on deletion."""
        if hasattr(self, 'connection') and self.connection:
            try:
                self.connection.close()
            except:
                pass
```
</template>

<steps>
1. Create new directory `isobar/io/yourdevice/`
2. Create `__init__.py` to export the device class
3. Create `output.py` with device implementation
4. Import OutputDevice base class
5. Implement all required methods (note_on, note_off, control, etc)
6. Add device-specific connection logic
7. Handle timing/clock if needed (ticks_per_beat property)
8. Add proper error handling and logging
9. Create helper methods for protocol formatting
10. Add to `isobar/io/__init__.py` if needed
11. Create tests in `tests/test_io_yourdevice.py`
12. Add documentation and examples
</steps>

<testing_template>
```python
import pytest
from unittest.mock import Mock, patch
import isobar as iso

@pytest.fixture
def mock_connection():
    """Mock the external connection."""
    with patch('isobar.io.yourdevice.output.create_connection') as mock:
        yield mock

def test_device_creation(mock_connection):
    """Test device initialization."""
    device = iso.YourOutputDevice("test_connection")
    assert device.param1 == "test_connection"
    mock_connection.assert_called_once()

def test_note_on_off(mock_connection):
    """Test note on/off events."""
    mock_conn = Mock()
    mock_connection.return_value = mock_conn
    
    device = iso.YourOutputDevice("test")
    device.note_on(60, 100, 0)
    device.note_off(60, 0)
    
    assert mock_conn.send.call_count == 2

def test_control_change(mock_connection):
    """Test control change events."""
    mock_conn = Mock()
    mock_connection.return_value = mock_conn
    
    device = iso.YourOutputDevice("test")
    device.control(7, 100, 0)  # Volume
    
    mock_conn.send.assert_called_once()

def test_value_validation(mock_connection):
    """Test MIDI value validation."""
    device = iso.YourOutputDevice("test")
    
    # Values should wrap to valid range
    device.note_on(200, 300, 20)  # Should become 72, 44, 4
    # Verify the wrapped values were sent

def test_timeline_integration():
    """Test with timeline."""
    device = iso.YourOutputDevice("test")
    timeline = iso.Timeline(output_device=device)
    
    timeline.schedule({
        "note": iso.PSequence([60, 64, 67]),
        "duration": 0.5
    })
    
    # Run briefly to test
    timeline.run(duration=2)
```
</testing_template>
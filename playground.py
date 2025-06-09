#!/usr/bin/env python3
"""
Isobar Playground - Quick MIDI Experimentation Environment

A ready-to-go environment for live coding and experimenting with isobar patterns.
Start coding immediately with pre-configured MIDI output and helpful shortcuts.

Usage:
    python playground.py

Quick Commands:
    play(pattern, **kwargs)     - Schedule pattern immediately
    stop_all()                  - Stop all playing tracks
    set_tempo(bpm)             - Change tempo
    show_devices()             - List available MIDI devices
    
Example:
    play(PSequence([60, 64, 67]), duration=0.5)
    play(PChoice([72, 75, 79]) + PRandom(-12, 12), channel=1)
"""

from isobar import *
import logging
import time
import atexit

# Global references for easy access
timeline = None
tracks = []

def setup():
    """Initialize the playground environment"""
    global timeline
    
    # Set up logging for feedback
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
    
    # Show available MIDI devices
    print("🎹 Isobar Playground - MIDI Experimentation Environment")
    print("=" * 60)
    show_devices()
    
    # Create timeline with error handling for stability
    timeline = Timeline(tempo=120, ignore_exceptions=True)
    timeline.start()
    
    print(f"\n✅ Timeline started at 120 BPM")
    print("💡 Type 'help_playground()' for commands and examples")
    
    # Cleanup on exit
    atexit.register(cleanup)

def show_devices():
    """Display available MIDI output devices"""
    from isobar.io import get_midi_output_names
    devices = get_midi_output_names()
    print(f"\n📱 Available MIDI Devices ({len(devices)}):")
    if devices:
        for i, name in enumerate(devices):
            print(f"  {i}: {name}")
    else:
        print("  No MIDI devices found. Consider:")
        print("  - Enable IAC Driver in Audio MIDI Setup (macOS)")
        print("  - Connect a hardware MIDI device")
        print("  - Use virtual MIDI software")

def play(pattern, duration=1, velocity=80, channel=0, **kwargs):
    """
    Quick function to play a pattern immediately
    
    Args:
        pattern: The pattern to play (note values)
        duration: Note duration pattern (default 1)
        velocity: Note velocity pattern (default 80)
        channel: MIDI channel (default 0)
        **kwargs: Additional track parameters
    
    Returns:
        Track reference for further manipulation
    """
    global timeline, tracks
    
    if timeline is None:
        print("❌ Timeline not initialized. Run setup() first.")
        return None
    
    # Build event dict
    event_dict = {
        "note": pattern,
        "duration": duration,
        "velocity": velocity,
        "channel": channel,
        **kwargs
    }
    
    # Schedule the pattern
    track = timeline.schedule(event_dict)
    tracks.append(track)
    
    print(f"🎵 Playing pattern on channel {channel}")
    return track

def stop_all():
    """Stop all currently playing tracks"""
    global timeline, tracks
    
    if timeline:
        for track in tracks:
            if track and hasattr(track, 'stop'):
                track.stop()
        tracks.clear()
        print("🛑 All tracks stopped")

def set_tempo(bpm):
    """Change the global tempo"""
    global timeline
    
    if timeline:
        timeline.tempo = bpm
        print(f"🎯 Tempo set to {bpm} BPM")

def cleanup():
    """Clean up resources on exit"""
    global timeline
    
    if timeline:
        stop_all()
        timeline.stop()
        print("\n👋 Playground session ended")

def help_playground():
    """Show playground commands and examples"""
    print("""
🎹 Isobar Playground Commands:

Basic Functions:
  play(pattern, **kwargs)     - Play a pattern immediately
  stop_all()                  - Stop all tracks
  set_tempo(bpm)             - Change tempo
  show_devices()             - List MIDI devices
  help_playground()          - Show this help

Quick Pattern Examples:
  
  # Simple sequences
  play(PSequence([60, 64, 67, 72]))
  play(PRange(60, 73))
  
  # Rhythmic patterns  
  play(PSequence([36]), duration=PBjorklund(3, 8))
  play(PChoice([60, 64, 67]), duration=PChoice([0.25, 0.5, 1]))
  
  # Random and evolving
  play(PChoice([60, 64, 67]) + PRandom(-12, 12))
  play(PBrown(60, 12, 2), duration=0.25)
  play(PWalk([60, 64, 67, 70], 1))
  
  # Multiple channels
  play(PSequence([36, 38]), channel=9)  # Drums
  play(PChoice([48, 50, 53]), channel=1, velocity=60)  # Bass
  
  # Control changes
  play(PSequence([60]), control={74: PSine(64, 32, 8)})  # Filter sweep
  
Common Pattern Classes:
  PSequence(list)            - Play list in order
  PChoice(list)              - Random choice from list  
  PRange(start, stop, step)  - Numeric range
  PRandom(min, max)          - Random numbers
  PBrown(start, max, step)   - Brownian motion
  PWalk(values, step_size)   - Random walk through values
  PBjorklund(hits, length)   - Euclidean rhythms
  PSine(center, amplitude, period) - Sine wave
  
Shortcuts for live coding:
  C4 = 60    # Middle C
  KICK = 36  # Standard kick drum
  SNARE = 38 # Standard snare drum
  
Try:
  play(PSequence([C4, C4+4, C4+7]), duration=0.5)
""")

# Helpful constants for live coding
C4 = 60
D4 = 62
E4 = 64
F4 = 65
G4 = 67
A4 = 69
B4 = 71
C5 = 72

KICK = 36
SNARE = 38
HIHAT = 42
OPENHAT = 46
CRASH = 49

# Auto-setup when imported or run as script
setup()

# Interactive mode when run as main script
if __name__ == "__main__":
    print("\n🚀 Quick Start Examples:")
    print("  play(PSequence([60, 64, 67, 72]))")
    print("  play(PChoice([60, 64, 67]) + PRandom(-12, 12), duration=0.25)")
    print("  play(PSequence([36]), duration=PBjorklund(3, 8), channel=9)")
    print("\n⌨️  Press Ctrl+C to exit")
    
    try:
        # Keep the script running for interactive use
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping playground...")
        cleanup()
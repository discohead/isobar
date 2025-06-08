# Debug Issue Prompt Template

When debugging isobar issues:

## Pattern Not Working
"Debug why pattern [name] is not producing expected output:
1. Test pattern in isolation with .all(10)
2. Check for StopIteration being raised early
3. Verify reset() properly initializes state
4. Ensure Pattern.value() used for nested patterns
5. Add logging to trace execution flow"

## Timeline/Track Issues
"Debug why events are not playing:
1. Verify timeline.running is True
2. Check output device is connected
3. Confirm track.playing is True
4. Test with DebugOutput device
5. Enable DEBUG logging
6. Check MIDI values are 0-127"

## Timing Problems
"Debug timing/tempo issues:
1. Log timeline.current_time progression
2. Check clock source configuration
3. Verify ticks_per_beat settings
4. Test with simple pattern first
5. Monitor actual vs expected BPM"

## Performance Issues
"Debug performance problems:
1. Profile with cProfile
2. Check for infinite patterns
3. Verify lazy evaluation is used
4. Look for unnecessary list conversions
5. Test with smaller parameters"
# Code Review Instructions

When reviewing isobar code, check for:

## Pattern Compliance
- ✅ Class names start with 'P'
- ✅ Has `abbreviation` attribute
- ✅ Implements `__next__()` and `reset()`
- ✅ Calls `super().reset()` in reset method
- ✅ Handles `Pattern.value()` for nested patterns

## Code Quality
- ✅ Docstring with examples
- ✅ Type hints on public methods
- ✅ MIDI values validated (0-127)
- ✅ Meaningful error messages
- ✅ No hardcoded timing values

## Common Mistakes
- ❌ Pattern storing Timeline reference
- ❌ Direct output device communication
- ❌ Missing reset() implementation
- ❌ Not supporting pattern parameters
- ❌ Using print() instead of logging

## Testing Coverage
- ✅ Basic functionality test
- ✅ Reset behavior test
- ✅ Operator overloading test
- ✅ Edge case handling
- ✅ StopIteration for finite patterns
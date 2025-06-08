# Refactor to Pattern Prompt Template

When refactoring code to follow isobar patterns:

## Pattern Refactoring
"Refactor this code to follow isobar pattern conventions:
- Rename class to start with 'P'
- Implement proper iterator protocol
- Add abbreviation attribute
- Support Pattern.value() for parameters
- Include reset() method
- Add operator overloading support"

## Make Iterator-Based
"Convert this list-based implementation to use lazy iteration:
- Replace pre-generated lists with on-demand generation
- Implement __next__ to generate values as needed
- Add proper state management in reset()
- Ensure memory efficiency for long sequences"

## Add Pattern Support
"Update this parameter to accept both static values and patterns:
- Use Pattern.value() to extract current value
- Support pattern arithmetic (addition, multiplication)
- Test with both static and pattern inputs
- Document pattern support in docstring"

## Extract to Output Device
"Extract output logic into proper OutputDevice:
- Create new class inheriting from OutputDevice
- Move protocol-specific code to new class
- Implement standard interface methods
- Add to timeline output device options"
# New Feature Prompt Template

When implementing a new feature for isobar:

## Pattern Feature
"Create a new pattern class P[Name] that [description]. It should:
- Accept [parameters] in __init__
- Generate values by [algorithm]
- Support [specific behavior]
- Include abbreviation '[abbr]'
- Follow isobar pattern conventions"

## Output Device Feature
"Create a new output device [Name]OutputDevice that:
- Connects to [system/protocol]
- Implements note_on, note_off, control methods
- Handles [specific requirements]
- Includes proper logging and error handling"

## Timeline Feature
"Add [feature] to Timeline/Track that:
- Allows [capability]
- Integrates with existing event system
- Maintains backward compatibility
- Includes tests for new functionality"

## Example Usage
Always include example usage:
```python
# Show how to use the new feature
timeline = Timeline()
result = timeline.new_feature(params)
```
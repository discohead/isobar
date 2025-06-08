# GitHub Copilot Instructions Guide

This directory contains instructions that guide GitHub Copilot when working with the isobar codebase.

## Structure

### Core Instructions (`copilot-instructions.md`)
The main file that Copilot reads for every interaction. Contains:
- Essential patterns (< 500 lines)
- Most common conventions
- Critical architecture rules

### Specialized Instructions (`instructions/`)
Focused guidance for specific tasks:
- `code-generation.instructions.md` - Creating new code
- `test-generation.instructions.md` - Writing tests
- `code-review.instructions.md` - Reviewing code

### Prompt Templates (`prompts/`)
Reusable templates for common tasks:
- `new-feature.prompt.md` - Adding features
- `refactor-to-pattern.prompt.md` - Refactoring code
- `debug-issue.prompt.md` - Debugging problems

## How It Works

1. **Copilot reads** `copilot-instructions.md` automatically
2. **You reference** specialized instructions for specific tasks
3. **You copy/adapt** prompts for common requests

## Usage Examples

### Creating a New Pattern
```python
# Copilot knows to:
# - Start class name with 'P'
# - Include abbreviation
# - Implement iterator protocol
# - Support operator overloading
```

### Writing Tests
```python
# Copilot automatically:
# - Uses pytest conventions
# - Tests basic, reset, operators
# - Handles edge cases
# - Mocks external resources
```

### Debugging
Reference the debug prompt:
"Debug why my pattern produces infinite values"

Copilot will suggest:
- Testing with .all(10)
- Checking reset() method
- Adding logging
- Validating logic

## Maintenance

Keep instructions updated when:
- New patterns are discovered
- Architecture changes
- Common mistakes identified
- Better practices emerge

Instructions are version controlled, so track changes over time.
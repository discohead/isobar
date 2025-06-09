# AI Assistant Setup Guide

This guide helps you set up and use the AI assistant configuration for the isobar project.

## Overview

The isobar project includes a comprehensive four-part AI assistant system:

1. **Claude Code** - Deep knowledge repository and context architecture
2. **Cursor** - Active behavioral rules during coding
3. **GitHub Copilot** - Persistent inline suggestions
4. **OpenAI Codex** - Cloud-based task automation and PR generation

Each component serves a specific purpose and they work together to enhance your development experience.

## Prerequisites

- [ ] Claude Code installed (claude.ai/code)
- [ ] Cursor IDE installed (optional but recommended)
- [ ] GitHub Copilot extension installed (for VS Code or your IDE)
- [ ] OpenAI Codex access (chatgpt.com/codex)

## Quick Start

### 1. Claude Code
The context is already generated. To use:
- Ask questions about the codebase architecture
- Request help with pattern creation
- Get debugging assistance

To update context after significant changes:
```bash
/user:context-update
```

### 2. Cursor
Rules are in `.cursor/rules/`. They automatically:
- Enforce naming conventions (P-prefix for patterns)
- Guide proper iterator implementation
- Suggest correct event scheduling syntax

### 3. GitHub Copilot
Instructions in `.github/copilot-instructions.md` help with:
- Pattern class structure
- Test generation
- Common isobar idioms

### 4. OpenAI Codex
AGENTS.md files throughout the codebase provide:
- Executable development commands
- Step-by-step task procedures
- Cross-references to other AI systems
- Debugging and validation workflows

## Development Workflows

### Creating a New Pattern
1. **Start with Copilot** - Get the basic structure
2. **Follow Cursor rules** - Ensure conventions are met
3. **Reference Claude Code** - See examples and patterns
4. **Use Codex for automation** - Generate tests and documentation

Example:
```python
# Copilot will suggest this structure
class PYourPattern(Pattern):
    abbreviation = "pyour"
    
    def __init__(self, param):
        self.param = param
        self.reset()
    
    def __next__(self):
        value = Pattern.value(self.param)
        # Your logic here
        return value
```

### Debugging Issues
1. Use the debug prompt templates in `.github/prompts/debug-issue.prompt.md`
2. Enable logging as suggested by AI assistants
3. Test patterns in isolation before timeline integration

### Live Coding
Always use these settings for stability:
```python
timeline = Timeline(tempo=120, ignore_exceptions=True, start=True)
```

## File Structure

```
.claude/
├── commands/           # Reusable Claude commands
└── ...

claude/
├── architecture/       # System design docs
├── technologies/       # Tech-specific patterns
├── workflows/          # Development workflows
└── ...

.cursor/
└── rules/             # MDC rule files
    ├── always/        # Core conventions
    ├── components/    # Component rules
    ├── features/      # Feature rules
    └── workflows/     # Workflow rules

.github/
├── copilot-instructions.md      # Main Copilot file
├── instructions/                 # Specialized guides
└── prompts/                     # Prompt templates

isobar/
├── AGENTS.md                    # Root task guide
├── */AGENTS.md                  # Module-specific tasks
└── ...                          # Source code
```

## Common Tasks

### Update AI Context
After major changes to the codebase:
```bash
/user:context-update    # Update Claude context
/user:rules-sync       # Sync Cursor rules
/user:instructions-optimize  # Optimize Copilot
# Update AGENTS.md files manually when adding modules
```

### Validate AI Guidance
Use the checklist in `ai_validation_checklist.md` to ensure:
- Pattern conventions are consistent
- No conflicting guidance between systems
- All systems provide appropriate suggestions

## Best Practices

1. **Use all four systems** - They complement each other
2. **Keep context updated** - Run updates quarterly
3. **Test AI suggestions** - Validate generated code
4. **Report issues** - Help improve the configuration

## Troubleshooting

### AI suggestions don't match patterns
- Run `/user:context-update` to refresh
- Check if CLAUDE.md has latest patterns

### Cursor rules not working
- Ensure `.cursor/rules/` exists
- Restart Cursor after changes

### Copilot ignoring conventions
- Check `.github/copilot-instructions.md` exists
- Restart your IDE

### Codex not finding context
- Ensure AGENTS.md files exist in relevant directories
- Check cross-references to CLAUDE.md, Cursor rules
- Verify repository access in Codex

## Maintenance Schedule

- **Weekly**: Review during team retrospectives
- **Monthly**: Update for new patterns
- **Quarterly**: Full context refresh
- **Annually**: Complete regeneration

## Further Reading

- `claude/workflows/` - Detailed workflow guides
- `.github/copilot-instructions-guide.md` - How instructions work
- `validation_report.md` - Integration test results
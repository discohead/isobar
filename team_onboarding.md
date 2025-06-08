# Team Onboarding: AI-Assisted Development

Welcome to isobar! This guide helps new team members understand and use our AI assistant configuration.

## Quick Start (5 minutes)

1. **Install AI Tools**
   - [ ] Claude Code from claude.ai/code
   - [ ] GitHub Copilot extension in your IDE
   - [ ] (Optional) Cursor IDE for enhanced rules

2. **Verify Setup**
   - [ ] Check `CLAUDE.md` exists (Claude context)
   - [ ] Check `.github/copilot-instructions.md` exists
   - [ ] Check `.cursor/rules/` directory exists

3. **Test AI Assistance**
   Create a new file and type:
   ```python
   class P
   ```
   You should see AI suggestions for pattern structure.

## Understanding the AI Ecosystem

### Three Layers of Assistance

1. **Copilot** (Immediate)
   - Inline code suggestions
   - Basic pattern templates
   - Quick fixes

2. **Cursor** (Active)
   - Real-time convention enforcement
   - Detailed implementation guidance
   - Context-aware rules

3. **Claude Code** (Deep)
   - Architecture explanations
   - Complex problem solving
   - Workflow guidance

### When to Use Each Tool

| Task | Tool | Why |
|------|------|-----|
| Writing new pattern | Start with Copilot | Quick structure |
| Implementing logic | Follow Cursor rules | Enforce conventions |
| Understanding architecture | Ask Claude Code | Deep context |
| Debugging | All three | Different perspectives |

## Your First Pattern

Let's create a pattern using AI assistance:

1. **Create file**: `my_pattern.py`

2. **Type**: `class P` and accept Copilot suggestion

3. **Follow the template**:
   ```python
   class PMyPattern(Pattern):
       abbreviation = "pmy"
       
       def __init__(self, values):
           self.values = values
           self.reset()
       
       def __next__(self):
           # Your logic here
           pass
       
       def reset(self):
           super().reset()
           self.index = 0
   ```

4. **Verify with checklist**:
   - [ ] Name starts with P
   - [ ] Has abbreviation
   - [ ] Implements __next__
   - [ ] Calls reset in __init__
   - [ ] reset calls super().reset()

## Common Workflows

### 1. Pattern Development
```bash
# See examples
cat claude/workflows/creating-patterns.md

# Get template
cat .claude/commands/create-pattern.md
```

### 2. Debugging
```bash
# See debugging guide
cat .claude/commands/debug-timeline.md

# Use debug prompts
cat .github/prompts/debug-issue.prompt.md
```

### 3. Live Coding
```python
# Always use these settings
timeline = Timeline(
    tempo=120,
    ignore_exceptions=True,  # Critical!
    start=True
)
```

## Key Conventions to Remember

### Pattern Naming
- ✅ `PSequence`, `PRandom`, `PMarkov`
- ❌ `Sequence`, `RandomPattern`, `MarkovChain`

### MIDI Validation
```python
note = int(note) % 128      # 0-127
velocity = int(velocity) % 128
channel = int(channel) % 16  # 0-15
```

### Event Scheduling
```python
timeline.schedule({
    "note": pattern_or_value,
    "duration": pattern_or_value,
    "velocity": pattern_or_value,
    "channel": 0-15
})
```

## Getting Help

1. **Quick questions**: Ask Copilot (comment your question)
2. **Implementation help**: Check Cursor rules
3. **Architecture questions**: Ask Claude Code
4. **Team help**: Check existing patterns in codebase

## Practice Tasks

### Task 1: Create a Simple Pattern
Create `PRepeat` that repeats a value N times.

### Task 2: Debug a Pattern
```python
# Why doesn't this work?
class PBroken(Pattern):
    def __init__(self, values):
        self.values = values
    
    def __next__(self):
        return self.values[0]
```

### Task 3: Use Timeline
Schedule your pattern to play middle C quarter notes.

## Resources

- **Patterns Guide**: `claude/discovered-patterns.md`
- **Architecture**: `claude/architecture/system-design.md`
- **Workflows**: `claude/workflows/`
- **Examples**: `examples/` directory

## Daily Workflow

1. **Morning**: Pull latest, check AI updates
2. **Coding**: Use all three AI tools
3. **Testing**: Follow test patterns
4. **Review**: Verify conventions met

## Tips from the Team

- "Always test patterns in isolation first"
- "Use `ignore_exceptions=True` for live coding"
- "Read existing patterns before creating new ones"
- "The AI knows our conventions - trust it"

## Next Steps

1. Read through `examples/00.ex-hello-world.py`
2. Try creating a pattern with AI assistance
3. Run the test suite to see patterns
4. Explore the `claude/` directory

Welcome to the team! 🎵
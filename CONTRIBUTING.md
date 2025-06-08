# Contributing

We welcome contributions to isobar! This guide will help you get started.

## Development Setup

1. Fork and clone the repository
2. Install in development mode:
   ```bash
   pip install -e .
   ```
3. Install test dependencies:
   ```bash
   pip install pytest pytest-timeout pytest-cov
   ```

## AI-Assisted Development

This project includes AI assistant configuration to help you write idiomatic isobar code:

- **Before coding**: Review patterns in `claude/discovered-patterns.md`
- **While coding**: Follow Cursor rules in `.cursor/rules/`
- **For guidance**: Use Copilot with `.github/copilot-instructions.md`

### Quick AI Checklist
When creating new patterns:
- [ ] Class name starts with 'P' (e.g., `PNewPattern`)
- [ ] Include `abbreviation` attribute
- [ ] Implement `__next__()` and `reset()`
- [ ] Support `Pattern.value()` for nested patterns
- [ ] Add comprehensive docstring with examples

## Code Style

### Naming Conventions
- Pattern classes: `PPatternName`
- Test functions: `test_pattern_name`
- Private methods: `_method_name`
- Constants: `UPPER_SNAKE_CASE`

### Pattern Structure
```python
class PExample(Pattern):
    """Brief description.
    
    Detailed explanation.
    
    Examples:
        >>> p = PExample(param)
        >>> p.all(4)
        [1, 2, 3, 4]
    """
    
    abbreviation = "pex"
    
    def __init__(self, param):
        self.param = param
        self.reset()
    
    def __next__(self):
        value = Pattern.value(self.param)
        # Logic here
        return result
```

To run a style check with flake8:

```
flake8 isobar
```

## Testing

To run unit tests:

```
python3 setup.py test
```

To generate a unit test coverage report:

```
pip3 install pytest-cov
pytest --cov=isobar tests
```

To automatically run unit tests on commit:
```
echo pytest > .git/hooks/pre-commit
```

### Writing Tests
Follow the patterns in `.github/instructions/test-generation.instructions.md`:
1. Test basic functionality
2. Test reset behavior
3. Test operator overloading
4. Test edge cases

Example:
```python
def test_pattern_basic():
    p = iso.PYourPattern(param)
    assert next(p) == expected
    assert p.all(4) == [1, 2, 3, 4]
```

## Documentation

To generate and serve the docs:

```
pip3 install mkdocs mkdocs-material
mkdocs serve
```

To deploy docs to GitHub:
```
mkdocs gh-deploy
```

To regenerate the per-class pattern docs for the pattern library docs and README:

```
auxiliary/scripts/generate-docs.py -m > docs/patterns/library.md
auxiliary/scripts/generate-docs.py
```

## Distribution

To push to PyPi:

* increment version in `setup.py`
* `git tag vx.y.z`, `git push --tags`, and create GitHub release
* `python3 setup.py sdist`
* `twine upload dist/isobar-x.y.z.tar.gz`

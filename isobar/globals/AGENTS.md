# AGENTS.md - isobar/globals

## Module Overview
Global state management and inter-process synchronization for isobar. This module handles shared parameters between processes and distributed instances.

## AI Context Integration
- **Deep context**: See `CLAUDE.md` in this directory for architectural details
- **Cursor rules**: Check `.cursor/rules/components/globals.mdc` for conventions
- **Copilot**: Uses `.github/instructions/globals.instructions.md` patterns

## Key Files
- `globals.py` - Global parameter storage (`GlobalStore` class)
- `sync.py` - Process synchronization utilities
- `__init__.py` - Public API exports

## Development Commands
```bash
# Run module-specific tests
pytest tests/test_globals.py -v

# Check for thread safety issues
python -m pytest tests/test_globals.py::test_concurrent_access

# Verify memory-mapped file cleanup
python -m pytest tests/test_globals.py::test_cleanup
```

## Testing Instructions
1. Test concurrent access patterns with multiple threads
2. Verify memory-mapped files are properly cleaned up
3. Check network sync latency under load
4. Ensure graceful degradation without sync services

## Common Tasks

### Adding a new global parameter type
1. Update `GlobalStore` in `globals.py`
2. Add validation in `set()` method
3. Update tests in `tests/test_globals.py`
4. Document in pattern examples

### Debugging sync issues
```bash
# Check active memory-mapped files
ls /tmp/isobar_*

# Monitor global parameter changes
python -c "from isobar.globals import GlobalStore; GlobalStore.monitor()"
```

## Code Pointers
- Global value storage: `GlobalStore` class in `globals.py`
- IPC mechanism: `ProcessSync` class in `sync.py`
- Pattern integration: `PGlobals` in `pattern/static.py`
- Network sync: `netglobals/` directory

## Validation Steps
1. Run `pytest tests/test_globals.py`
2. Check no orphaned memory-mapped files in `/tmp/`
3. Verify thread-safe operations with concurrent test
4. Test network sync with multiple processes
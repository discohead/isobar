# CLAUDE.md - isobar/globals

This directory contains global state management and inter-process synchronization components.

## Module Overview

The `globals` module provides mechanisms for sharing parameters between processes and synchronizing state across distributed isobar instances. This is crucial for multi-process compositions and networked performances.

## Core Components

### globals.py
- **Purpose**: Global parameter storage and retrieval
- **Key Classes**: 
  - `GlobalStore`: Central storage for global parameters
  - `PGlobals`: Pattern class for accessing global values
- **Usage**: Allows patterns to reference shared values that can be modified in real-time

### sync.py
- **Purpose**: Process synchronization utilities
- **Key Features**:
  - Memory-mapped file support for IPC
  - Lock-free data structures where possible
  - Network synchronization protocols

## Key Design Principles

1. **Thread Safety**: All global operations must be thread-safe
2. **Performance**: Use memory-mapped files for efficient IPC
3. **Flexibility**: Support both local and networked synchronization
4. **Real-time**: Minimize latency for live performance

## Common Patterns

### Using Global Parameters
```python
# Set a global value
GlobalStore.set("tempo_multiplier", 1.5)

# Use in a pattern
pattern = PSequence([60, 64, 67]) * PGlobals("tempo_multiplier")
```

### Process Synchronization
```python
# Sync between processes
sync = ProcessSync("composition_1")
sync.set_parameter("section", "verse")

# In another process
section = sync.get_parameter("section")
```

## Implementation Notes

- Global values are stored in shared memory for performance
- Network sync uses efficient binary protocols
- All synchronization is non-blocking where possible
- Graceful degradation if sync services unavailable

## Testing Considerations

- Test concurrent access patterns
- Verify memory-mapped file cleanup
- Test network sync with latency
- Ensure no memory leaks in long-running processes

## Related Modules

- `netglobals/`: Network-based global parameter sharing
- `netclock/`: Network clock synchronization
- `PGlobals` pattern in `pattern/static.py`
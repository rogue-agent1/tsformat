# tsformat

Timestamp converter between formats. Zero dependencies.

## Commands

```bash
tsformat now                     # Current time in all formats
tsformat now --unix              # Unix timestamp
tsformat now --iso               # ISO 8601
tsformat convert 1700000000      # Unix → all formats
tsformat convert "2024-01-01"    # ISO → all formats
tsformat convert "30m ago"       # Relative → all formats
tsformat diff 1700000000 1700100000  # Time difference
```

## Formats

Unix (s/ms), ISO 8601, local, human-readable, relative

## Requirements

- Python 3.6+ (stdlib only)

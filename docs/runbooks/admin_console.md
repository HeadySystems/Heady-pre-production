# Admin Console Runbook

## Overview
The admin console (`admin_console.py`) performs health, structure, dependency, and
security audits. It is also responsible for configuration audits of
`render.yaml` and `mcp_config.json`.

## Prerequisites
- Python 3.9+
- Project dependencies installed (`pip install -r requirements.txt`)

## Common Commands
Run a full audit from the repository root:
```
python admin_console.py
```

Run a specific check:
```
python admin_console.py --check health
python admin_console.py --check structure
python admin_console.py --check deps
python admin_console.py --check security
python admin_console.py --check config
```

Write results to a JSON file:
```
python admin_console.py --output audit.json
```

## Interpretation Guidance
- `security.config_audit.issue_count`: non-zero indicates placeholders or
  hard-coded values in configuration files.
- `dependencies`: lists installed packages; use for confirming runtime
  requirements are present.

## Rollback
If an audit fails unexpectedly, revert the last change to `admin_console.py` or
`src/config_audit.py`, then re-run the audit. No other systems are affected.

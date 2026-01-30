# Configuration Audit Guide

## Purpose
The configuration audit checks `render.yaml` and `mcp_config.json` for
hard-coded secrets and ensures sensitive keys use environment variable
placeholders.

## Sensitive Keys
The audit currently tracks:
- `DATABASE_URL`
- `HF_TOKEN`
- `HEADY_API_KEY`
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `REMOTE_GPU_HOST`
- `REMOTE_GPU_PORT`
- `GPU_MEMORY_LIMIT`
- `ENABLE_GPUDIRECT`

## Running the Audit
```
python admin_console.py --check config
```

## Expected Output
The output includes `render_yaml_issues` and `mcp_config_issues`. Each issue
records the key, value, and path within the configuration file.

## Mitigation
If issues are reported:
1. Replace the value with `${ENV_VAR_NAME}`.
2. Add the environment variable to your deployment secrets.
3. Re-run the audit to confirm the issue count is zero.

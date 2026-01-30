from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

SENSITIVE_ENV_KEYS = {
    "DATABASE_URL",
    "HF_TOKEN",
    "HEADY_API_KEY",
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_ACCOUNT_ID",
    "REMOTE_GPU_HOST",
    "REMOTE_GPU_PORT",
    "GPU_MEMORY_LIMIT",
    "ENABLE_GPUDIRECT",
}

SECRET_PATTERN = re.compile(
    r"(hf_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z\-_]{20,}|sk-[A-Za-z0-9]{20,}|"
    r"-----BEGIN (?:RSA|EC|OPENSSH) PRIVATE KEY-----)"
)


def _is_placeholder(value: str) -> bool:
    return value.strip().startswith("${") and value.strip().endswith("}")


def _maybe_issue(
    *,
    file: Path,
    key: str,
    value: str,
    message: str,
    path: Optional[str] = None,
) -> Dict[str, str]:
    issue = {
        "file": str(file),
        "key": key,
        "value": value,
        "message": message,
    }
    if path:
        issue["path"] = path
    return issue


def audit_render_yaml(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    issues: List[Dict[str, str]] = []
    services = data.get("services", [])
    for idx, service in enumerate(services):
        env_vars = service.get("envVars", [])
        for env_idx, env in enumerate(env_vars):
            if isinstance(env, dict) and "key" in env and "value" in env:
                key = str(env["key"])
                value = str(env["value"])
                env_path = f"services[{idx}].envVars[{env_idx}]"
                if key in SENSITIVE_ENV_KEYS and not _is_placeholder(value):
                    issues.append(
                        _maybe_issue(
                            file=path,
                            key=key,
                            value=value,
                            message="Sensitive env var should use placeholder.",
                            path=env_path,
                        )
                    )
                if SECRET_PATTERN.search(value):
                    issues.append(
                        _maybe_issue(
                            file=path,
                            key=key,
                            value=value,
                            message="Possible hard-coded secret detected.",
                            path=env_path,
                        )
                    )
    return issues


def audit_mcp_config(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    issues: List[Dict[str, str]] = []
    servers = data.get("mcpServers", {})
    for server_name, server in servers.items():
        env = server.get("env", {})
        if not isinstance(env, dict):
            continue
        for key, value in env.items():
            value_str = str(value)
            env_path = f"mcpServers.{server_name}.env.{key}"
            if key in SENSITIVE_ENV_KEYS and not _is_placeholder(value_str):
                issues.append(
                    _maybe_issue(
                        file=path,
                        key=key,
                        value=value_str,
                        message="Sensitive env var should use placeholder.",
                        path=env_path,
                    )
                )
            if SECRET_PATTERN.search(value_str):
                issues.append(
                    _maybe_issue(
                        file=path,
                        key=key,
                        value=value_str,
                        message="Possible hard-coded secret detected.",
                        path=env_path,
                    )
                )
    return issues


def audit_configurations(project_root: Path) -> Dict[str, Any]:
    render_path = project_root / "render.yaml"
    mcp_path = project_root / "mcp_config.json"
    render_issues = audit_render_yaml(render_path)
    mcp_issues = audit_mcp_config(mcp_path)
    return {
        "render_yaml_issues": render_issues,
        "mcp_config_issues": mcp_issues,
        "issue_count": len(render_issues) + len(mcp_issues),
    }

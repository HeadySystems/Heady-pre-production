from pathlib import Path

import src.config_audit as config_audit


def test_audit_render_yaml_detects_placeholder(tmp_path: Path) -> None:
    render_yaml = tmp_path / "render.yaml"
    render_yaml.write_text(
        """
services:
  - type: web
    name: test
    envVars:
      - key: HF_TOKEN
        value: "actual-secret"
"""
    )
    issues = config_audit.audit_render_yaml(render_yaml)
    assert issues
    assert issues[0]["key"] == "HF_TOKEN"


def test_audit_mcp_config_allows_placeholders(tmp_path: Path) -> None:
    mcp_config = tmp_path / "mcp_config.json"
    mcp_config.write_text(
        """
{
  "mcpServers": {
    "cloudflare": {
      "env": {
        "CLOUDFLARE_API_TOKEN": "${CLOUDFLARE_API_TOKEN}"
      }
    }
  }
}
"""
    )
    issues = config_audit.audit_mcp_config(mcp_config)
    assert issues == []

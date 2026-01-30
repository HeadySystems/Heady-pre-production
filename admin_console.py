#!/usr/bin/env python3
"""
Admin Console for Heady Project
Implements audit and system health checks
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import psutil
import platform

from src.config_audit import audit_configurations

def log_info(msg):
    print(f"[INFO] {datetime.now().isoformat()} {msg}")

def log_error(msg):
    print(f"[ERROR] {datetime.now().isoformat()} {msg}", file=sys.stderr)

def run_command(cmd, cwd=None, timeout=120):
    """Execute command with timeout and error handling"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, timeout=timeout,
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        log_error(f"Command timed out: {cmd}")
        raise
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {cmd}")
        log_error(f"stdout: {e.stdout}")
        log_error(f"stderr: {e.stderr}")
        raise

def check_system_health():
    """Check system health and resources"""
    health_info = {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": dict(psutil.disk_usage('/')._asdict())
    }
    return health_info

def check_project_structure(project_root):
    """Audit project directory structure"""
    required_dirs = ["src", "tests", "docs"]
    required_files = ["requirements.txt", "README.md", "admin_console.py"]

    structure_info = {
        "exists": project_root.exists(),
        "missing_dirs": [],
        "missing_files": []
    }

    for d in required_dirs:
        if not (project_root / d).is_dir():
            structure_info["missing_dirs"].append(d)

    for f in required_files:
        if not (project_root / f).exists():
            structure_info["missing_files"].append(f)

    return structure_info

def check_dependencies(project_root):
    """Check installed dependencies against requirements.txt"""
    deps_info = {"installed": [], "missing": [], "python_packages": []}

    requirements_txt = project_root / "requirements.txt"
    if requirements_txt.exists():
        try:
            stdout, _ = run_command("pip list --format=json")
            pip_data = json.loads(stdout)
            installed = {pkg["name"].lower(): pkg["version"] for pkg in pip_data}

            with open(requirements_txt) as f:
                required = [line.strip().split("==")[0].lower()
                           for line in f if line.strip() and not line.startswith("#")]

            deps_info["python_packages"] = [
                pkg for pkg in required if pkg in installed
            ]
        except Exception as e:
            log_error(f"Failed to get Python packages: {e}")

    return deps_info

def check_security(project_root):
    """Security audit checks"""
    security_info = {
        "has_env_file": (project_root / ".env").exists(),
        "has_env_example": (project_root / ".env.example").exists(),
        "has_env_template": (project_root / ".env.template").exists(),
        "secrets_in_config": [],
        "file_permissions": {},
        "config_audit": {}
    }

    # Check for hardcoded secrets in config files
    config_files = ["mcp_config.json", "render.yaml", "package.json"]
    for config_file in config_files:
        config_path = project_root / config_file
        if config_path.exists():
            try:
                with open(config_path) as f:
                    content = f.read()
                    if "password" in content.lower() or "token" in content.lower():
                        security_info["secrets_in_config"].append(config_file)
            except Exception as e:
                log_error(f"Failed to check {config_file}: {e}")

    security_info["config_audit"] = audit_configurations(project_root)

    return security_info

def audit_project(project_root):
    """Main audit orchestration"""
    log_info(f"Starting audit for project: {project_root}")

    audit_info = {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "project_root": str(project_root),
        "system_health": check_system_health(),
        "project_structure": check_project_structure(project_root),
        "dependencies": check_dependencies(project_root),
        "security": check_security(project_root)
    }

    log_info("Audit completed successfully")
    return audit_info

def main():
    parser = argparse.ArgumentParser(description="Admin console audit")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                        help="Project root directory")
    parser.add_argument("--output", type=Path, help="Output audit info to file")
    parser.add_argument("--check", choices=["health", "structure", "deps", "security", "config"],
                       help="Run specific check only")

    args = parser.parse_args()

    try:
        if args.check == "health":
            result = check_system_health()
        elif args.check == "structure":
            result = check_project_structure(args.project_root)
        elif args.check == "deps":
            result = check_dependencies(args.project_root)
        elif args.check == "security":
            result = check_security(args.project_root)
        elif args.check == "config":
            result = audit_configurations(args.project_root)
        else:
            result = audit_project(args.project_root)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            log_info(f"Audit info written to {args.output}")
        else:
            print(json.dumps(result, indent=2))

        return 0
    except Exception as e:
        log_error(f"Audit failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

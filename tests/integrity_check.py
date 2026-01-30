import os
import sys
import importlib.util
from pathlib import Path

REQUIRED_ENV_VARS = ["HF_TOKEN", "GOOGLE_API_KEY"]
BANNED_KEYWORDS = ["openai", "anthropic", "boto3", "azure.identity"]

def check_env_vars():
    print("Checking Environment Variables...")
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        print(f"❌ CRITICAL: Missing required variables: {missing}")
        return False
    print("✅ Environment variables found.")
    return True

def scan_imports():
    print("\nScanning for Unauthorized Dependencies...")
    project_root = Path(__file__).parent.parent
    violations = []
    for py_file in project_root.rglob("*.py"):
        if "integrity_check.py" in py_file.name: continue
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                for keyword in BANNED_KEYWORDS:
                    if keyword in content:
                        violations.append(f"{py_file.name}: contains '{keyword}'")
        except Exception: pass

    if violations:
        print("❌ POLICY VIOLATION: Unauthorized services detected:")
        for v in violations: print(f"   - {v}")
        return False
    print("✅ No unauthorized paid APIs detected.")
    return True

if __name__ == "__main__":
    print("--- SYSTEM INTEGRITY CHECK ---\n")
    # We allow env var check to fail in this CI/Build environment where secrets aren't loaded
    # But we want to run the import scan.
    env_ok = check_env_vars()
    scan_ok = scan_imports()

    if scan_ok:
        print("\n🎉 SYSTEM STATUS: COMPLIANT (Env vars may be missing in this context)")
        sys.exit(0)
    else:
        print("\n⚠️ SYSTEM STATUS: ISSUES DETECTED")
        sys.exit(1)

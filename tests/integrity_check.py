import os
import sys

BANNED_KEYWORDS = ["openai", "anthropic", "aws"]
EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", "venv"}
EXCLUDED_FILES = {"LICENSE", "package-lock.json"}

def scan_files():
    found_violations = False
    for root, dirs, files in os.walk("."):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if file in EXCLUDED_FILES:
                continue

            file_path = os.path.join(root, file)
            # Skip this script itself
            if os.path.abspath(file_path) == os.path.abspath(__file__):
                continue

            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read().lower()
                    for keyword in BANNED_KEYWORDS:
                        if keyword in content:
                            print(f"VIOLATION: Found banned keyword '{keyword}' in {file_path}")
                            found_violations = True
            except Exception as e:
                print(f"WARNING: Could not read {file_path}: {e}")

    return found_violations

if __name__ == "__main__":
    print("Starting integrity check...")
    if scan_files():
        print("Integrity check FAILED: Banned keywords found.")
        sys.exit(1)
    else:
        print("Integrity check PASSED.")
        sys.exit(0)

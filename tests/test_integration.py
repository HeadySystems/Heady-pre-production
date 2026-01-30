import os
import pytest
from src.heady_project.execute_build import build_manifest

def test_build_manifest(tmp_path):
    # Create a dummy projects.json
    p_file = tmp_path / "projects.json"
    p_file.write_text('[{"name": "test"}]')

    # Run build (which currently writes to cwd/heady-manifest.json)
    # We should ideally refactor build_manifest to accept output path,
    # but for now we clean up.

    manifest = build_manifest(str(p_file), "http://test.repo", "v1.0")

    assert manifest["version"] == "v1.0"

    # Clean up artifact if it exists in CWD
    if os.path.exists("heady-manifest.json"):
        os.remove("heady-manifest.json")

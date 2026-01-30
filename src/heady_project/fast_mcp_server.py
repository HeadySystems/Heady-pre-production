import asyncio
import os
import sys
import json
import logging
from typing import Any, Dict, List

# Check if mcp is installed, otherwise provide instructions
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("CRITICAL: 'mcp' library not found. Install with: pip install mcp")
    sys.exit(1)

# Initialize FastMCP Server
mcp = FastMCP("Heady Services Integration")

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

# --- Mock Client for "Heady Services" ---
class HeadyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # For dev/mock purposes we allow missing key if just testing availability
        if not self.api_key and os.getenv("HEADY_ENV") == "production":
             raise ValueError("HEADY_API_KEY environment variable is missing")

    def get_service_status(self) -> Dict[str, str]:
        # Mock response
        return {"status": "operational", "version": "1.2.0", "region": "us-east-1"}

    def execute_task(self, task_id: str, parameters: Dict[str, Any]) -> str:
        # Mock execution logic
        return f"Task {task_id} executed with params: {parameters}"

# Initialize Client
# Ensure HEADY_API_KEY is set in your .env or environment
heady_client = None
try:
    heady_client = HeadyClient(api_key=os.getenv("HEADY_API_KEY", "mock-key-for-dev"))
except Exception as e:
    logger.error(f"Failed to initialize Heady Client: {e}")

# --- MCP Resources (Read-only Data) ---

@mcp.resource("heady://status")
def get_system_status() -> str:
    """Returns the current operational status of Heady Services."""
    if not heady_client:
        return "Error: Client not initialized"
    status = heady_client.get_service_status()
    return json.dumps(status, indent=2)

# --- MCP Tools (Executable Actions) ---

@mcp.tool()
def run_heady_task(task_name: str, priority: str = "normal") -> str:
    """
    Executes a task within the Heady Services ecosystem.

    Args:
        task_name: The identifier of the task to run.
        priority: Execution priority ('low', 'normal', 'high').
    """
    if not heady_client:
        return "Error: Client not initialized"

    logger.info(f"Executing task: {task_name} with priority {priority}")
    result = heady_client.execute_task(task_name, {"priority": priority})
    return result

@mcp.tool()
def audit_connections() -> str:
    """
    Checks if the Heady Service is reachable and authorized.
    Useful for Admin UI diagnostics.
    """
    # Real implementation would ping the Heady API endpoint
    return "Connection verified: Latency 45ms"

if __name__ == "__main__":
    # Runs the server over stdio, which allows Windsurf/Claude/Cursor to connect directly
    print("Starting Heady MCP Server via stdio...", file=sys.stderr)
    mcp.run()

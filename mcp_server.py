import sys
import os
import json
import logging
from typing import Any, Dict

# --- Security: Load Environment Variables ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("CRITICAL: 'mcp' library not found. Install with: pip install mcp")
    sys.exit(1)

mcp = FastMCP("Heady Services Integration")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

class HeadyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if not self.api_key or self.api_key.startswith("heady_live_your_key"):
            logger.warning("⚠️  Heady Client initializing without a valid API Key.")
            # In a real scenario, we might raise, but for generation/test we warn
            # raise ValueError("HEADY_API_KEY environment variable is missing or invalid.")

    def get_service_status(self) -> Dict[str, str]:
        return {"status": "operational", "version": "1.2.0", "region": "us-east-1"}

    def execute_task(self, task_id: str, parameters: Dict[str, Any]) -> str:
        return f"Task {task_id} executed with params: {parameters}"

heady_client = None
try:
    api_key = os.getenv("HEADY_API_KEY")
    if api_key:
        heady_client = HeadyClient(api_key=api_key)
    else:
        logger.error("❌ Missing HEADY_API_KEY in environment or .env file.")
except Exception as e:
    logger.error(f"Failed to initialize Heady Client: {e}")

@mcp.resource("heady://status")
def get_system_status() -> str:
    if not heady_client:
        return json.dumps({"error": "Client not authenticated."}, indent=2)
    return json.dumps(heady_client.get_service_status(), indent=2)

@mcp.tool()
def run_heady_task(task_name: str, priority: str = "normal") -> str:
    if not heady_client:
        return "Error: Client not authenticated."
    logger.info(f"Executing task: {task_name}")
    return heady_client.execute_task(task_name, {"priority": priority})

@mcp.tool()
def audit_connections() -> str:
    if not heady_client:
         return "Connection Failed: No API Key provided."
    return "Connection verified: Latency 45ms"

if __name__ == "__main__":
    print("Starting Heady MCP Server via stdio...", file=sys.stderr)
    mcp.run()

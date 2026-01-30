import os
import sys
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Ensure we can import from src
# Assuming this script is run as "python src/heady_project/heady_mcp_server.py"
# or similar, we need to add the repo root to sys.path.
# The repo root is 2 levels up from this file.
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.append(repo_root)

# Import internal services
from src.heady_project.economy import mint_coin
from src.heady_project.archive import HeadyArchive
from src.heady_project.nlp_service import nlp_service

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Heady MCP Server")

@mcp.tool()
def mint_currency(amount: int, currency_type: str = "HeadyCoin") -> str:
    """
    Mints a specified amount of currency.

    Args:
        amount: The amount to mint.
        currency_type: The name of the currency (default: HeadyCoin).
    """
    result = mint_coin(amount, currency_type)
    if result:
        return f"Successfully minted. Transaction ID: {result}"
    return "Minting failed. Check logs for details."

@mcp.tool()
def archive_data(data: dict, destination: str) -> str:
    """
    Preserves (archives) project data to a specified destination.

    Args:
        data: A dictionary containing the data to archive.
        destination: The target path or identifier for the archive.
    """
    success = HeadyArchive.preserve(data, destination)
    return "Data preservation successful" if success else "Data preservation failed"

@mcp.tool()
def summarize_text(text: str) -> str:
    """
    Summarizes the given text using the internal NLP service.

    Args:
        text: The text to summarize.
    """
    return nlp_service.summarize_text(text)

@mcp.tool()
def ask_ai(prompt: str) -> str:
    """
    Generates a response to a prompt using the internal NLP service.

    Args:
        prompt: The input prompt for the AI.
    """
    return nlp_service.generate_response(prompt)

if __name__ == "__main__":
    mcp.run()

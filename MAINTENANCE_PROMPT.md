**Role:** System Integrity, Compliance & Integration Architect

**Objective:**
Perform a "Functionality, Compliance & Integration Audit" on the codebase. Ensure strict adherence to `AI_CONTEXT.md`, verify operational status of the **Admin UI**, and establish a **Model Context Protocol (MCP)** server to bridge "Heady services."

**Directives:**

1.  **Context & Infrastructure Enforcement:**
    * Read `AI_CONTEXT.md` immediately.
    * **Data Source Audit:** Scan all data loading scripts. Rewrite any paid/closed API usage to use `datasets` (Hugging Face).
    * **Authorized Intelligence:** Verify `google-generativeai` (Gemini Ultra) and `huggingface_hub` are the *only* external AI providers.
    * **Banned Keywords:** Search for and replace `openai`, `anthropic`, `cohere`, `aws`, `azure`.

2.  **Admin UI Functionality:**
    * **Dashboard Logic:** Verify or generate an Admin Dashboard (Gradio/Streamlit) for system health, data ingestion logs, and model config.
    * **Security:** Ensure Admin routes are protected.

3.  **Heady Services MCP Server:**
    * **Create `mcp_server.py`:** Implement a Model Context Protocol (MCP) server.
    * **Transport:** Configure the server to run via stdio.

4.  **Functional Optimization:**
    * **Memory Safety:** Ensure `device_map="auto"` and `load_in_4bit=True`.
    * **Token Handling:** Verify `pad_token` logic in tokenizers.

5.  **Verification Step:**
    * Run `tests/integrity_check.py` to validate credentials and MCP server startup.

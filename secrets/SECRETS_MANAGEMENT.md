# Secrets Management & Security Protocol

This project relies on strict segregation of sensitive credentials. **NEVER commit actual API keys to version control.**

## 1. Required Secrets Checklist

You must define the following environment variables for the system to function:

| **Variable Name** | **Service** | **Purpose** | **Acquisition Method** |
| **\`HF_TOKEN\`** | Hugging Face | Access to Pro/Enterprise Inference Endpoints and gated models (Llama 3, etc.). | [Settings > Access Tokens](https://huggingface.co/settings/tokens) (Read/Write) |
| **\`GOOGLE_API_KEY\`** | Google Cloud | Access to Gemini Ultra/Advanced models. | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| **\`HEADY_API_KEY\`** | Heady Services | Authenticating with the internal Heady ecosystem. | Request from Heady Admin / DevOps |
| **\`GH_TOKEN\`** | GitHub | (Optional) Automated CI/CD actions or package registry access. | GitHub Developer Settings |

## 2. Implementation Methods

### A. Local Development (The \`.env\` Method)

We use the \`python-dotenv\` library to load secrets from a local file into environment variables.

1. **Create the file:** Copy \`.env.template\` to a new file named \`.env\`.
   \`\`\`
   cp .env.template .env
   \`\`\`
2. **Fill it:** Open \`.env\` and paste your actual keys.
3. **Secure it:** Ensure \`.env\` is listed in your \`.gitignore\` file (already configured, but verify).

### B. GitHub Codespaces / Actions
Do not use an \`.env\` file here. Use **Repository Secrets**.

### C. Hugging Face Spaces
If deploying the Admin UI or MCP server to a generic Space:
1. Go to **Settings** in your HF Space.
2. Scroll to **Variables and secrets**.
3. Add "New Secret".

## 3. Security Best Practices
* **Audit Logging:** The \`mcp_server.py\` is configured to log *usage* but masking the actual key values.
* **Rotation:** Rotate the \`HEADY_API_KEY\` every 90 days.
* **Least Privilege:** Ensure the \`HF_TOKEN\` only has permissions for the specific repositories needed.

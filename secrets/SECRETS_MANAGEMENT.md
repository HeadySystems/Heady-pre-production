# Secrets Management & Security Protocol

This project relies on strict segregation of sensitive credentials. **NEVER commit actual API keys to version control.**

## 1. Required Secrets Checklist

| Variable Name | Service | Purpose | Acquisition Method |
| :--- | :--- | :--- | :--- |
| **\`HF_TOKEN\`** | Hugging Face | Access to Pro/Enterprise Inference Endpoints. | [Settings > Access Tokens](https://huggingface.co/settings/tokens) |
| **\`GOOGLE_API_KEY\`** | Google Cloud | Access to Gemini Ultra/Advanced. | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| **\`HEADY_API_KEY\`** | Heady Services | Authenticating with internal ecosystem. | Request from Admin |
| **\`GH_TOKEN\`** | GitHub | (Optional) CI/CD actions. | GitHub Developer Settings |

## 2. Implementation Methods
### A. Local Development (The .env Method)
1. Copy \`.env.template\` to \`.env\`.
2. Fill in your keys.
3. Ensure \`.env\` is in \`.gitignore\`.

### B. GitHub Codespaces / Actions
Use **Repository Secrets** in Settings > Secrets and variables > Actions.

## 3. Security Best Practices
* **Audit Logging:** The \`mcp_server.py\` logs usage but masks key values.
* **Rotation:** Rotate keys regularly.

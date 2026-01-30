# Heady Data Processing Framework

Heady is a Python-based data-processing framework designed to manage project manifests, archives, and audits. It provides a CLI for building manifests from configuration files and an Admin UI for system management.

## Architecture

The project is consolidated under `src/heady_project/` and includes the following modules:
- `api.py`: FastAPI backend for the Admin UI.
- `execute_build.py`: Main script for building manifests from `projects.json`.
- `consolidated_builder.py`: Internal logic for build steps and archiving.
- `admin_console.py`: CLI tool for administrative tasks.
- `nlp_service.py`: Hugging Face transformers integration for AI features.
- `frontend/`: React-based Admin UI.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd Heady
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Ensure `projects.json` exists (see `projects.json.example`).
   Set environment variables as needed (e.g., `HEADY_VERSION`).

## Usage

### Admin UI
Start the backend server:
```bash
uvicorn src.heady_project.api:app --reload
```
Access the UI at `http://localhost:8000`. The UI includes AI features for log summarization and code assistance powered by Hugging Face models (T5, DistilGPT2).

### CLI Tools
Build Manifest:
```bash
python -m src.heady_project.execute_build --repo-url "http://example.com" --version "v1.0"
```

Admin Console:
```bash
python -m src.heady_project.admin_console --action full_audit
```

## Cloud / GPU Execution
To run this project on Google Colab and utilize free GPU resources for AI tasks:
1. See [COLAB_PROTOCOL.md](COLAB_PROTOCOL.md) for detailed instructions.
2. Use the `notebooks/Heady_Colab_Protocol.ipynb` notebook.

## Testing
Run tests using pytest:
```bash
pytest
```

## Development Scripts

### Available Scripts
- `npm start` – Start the server
- `python src/process_data.py` – Run Python worker standalone
- `python admin_console.py` – Run system audit
- `python src/process_data.py qa` – Test QA interface

### Testing
```bash
# Test Python worker QA functionality
echo '{"question":"What is Heady?","context":"Heady is a system"}' | python src/process_data.py qa

# Run system audit
python admin_console.py --output audit.json

# Run config-only audit
python admin_console.py --check config

# Run Python unit tests
python -m pytest
```

## Copilot Customization

- `.github/copilot-instructions.md` – Project overview and Quiz Protocol for documentation
- `.github/copilot-mcp-config.json` – MCP server definitions
- `.github/workflows/copilot-setup-steps.yml` – Setup workflow for Copilot

## Documentation Protocol

All documentation follows the **Quiz & Flashcard Methodology** (see `.github/copilot-instructions.md`).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the code style guidelines in `.github/copilot-instructions.md`
4. Ensure all tests pass
5. Submit a pull request

## License

See LICENSE file.

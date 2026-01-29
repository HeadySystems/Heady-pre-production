# Project Summary
The Heady repo is a Python‑based data‑processing framework. It includes a Render blueprint (render.yaml), Model Context Protocol configuration (mcp_config.json), and Python scripts such as execute_build.py, consolidated_builder.py and admin_console.py. The build script processes a projects.json file to produce heady-manifest.json files and the admin console can build, serve an API and perform audits. The repository currently has only a one‑line README and a placeholder agent description file under .github/agents.

# Languages and Tools
The project is primarily written in Python (version 3.8+), with YAML and JSON configuration files. The build process uses standard Python tooling (pip install, python <script>). The Render blueprint calls pip install -r requirements.txt, so note that a requirements.txt file must be maintained.
Git is used for cloning repositories.
Certain environment variables (DATABASE_URL, OTHER_API_KEY) and secrets (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID) must be provided.

# Build, Test and Run
1. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the build script**:
   ```bash
   python execute_build.py --repo-url <repo_url> --zip-file <zip_file> --build-script <build_script>
   ```
4. **Run the consolidated builder**:
   ```bash
   python HeadySystems/heady_project/src/consolidated_builder.py
   ```
5. **Run the admin console**:
   ```bash
   python HeadySystems/heady_project/src/admin_console.py --action <builder_build|full_audit|serve_api>
   ```
6. **Run tests**:
   Tests should live in a `tests/` folder and can be run with pytest:
   ```bash
   pytest
   ```

# Important Architecture and Config
- Key source files: `HeadySystems/heady_project/src`, `heady_demo_kit/heady_project/src`
- Render blueprint: `render.yaml`
- MCP configuration: `mcp_config.json` (defines server definitions and secrets)
- Copilot Agent Template: `.github/agents/copilot-insturctions.agent.md`
- Workflow file will be added.

# Non-obvious Dependencies
The build script requires the `zipfile` module (part of Python standard library), external `git` and `zip` tools, and a `projects.json` file in the repository root.

# Hugging Face CLI and Jobs
This project may use Hugging Face Jobs. Below are instructions for using the CLI.

1. **Install the Hugging Face CLI**:

   Using PowerShell:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://hf.co/cli/install.ps1 | iex"
   ```

   Using uv:
   ```bash
   uv tool install hf
   ```

2. **Login to your Hugging Face account**:
   ```bash
   hf auth login
   ```

3. **Create a job using the hf jobs command**:

   Run Python code directly:
   ```bash
   hf jobs run python:3.12 python -c 'print("Hello from the cloud!")'
   ```

   Use GPUs without any setup:
   ```bash
   hf jobs run --flavor a10g-small pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel \
     python -c "import torch; print(torch.cuda.get_device_name())"
   ```

   Run from Hugging Face Spaces (using Docker):
   ```bash
   hf jobs run hf.co/spaces/lhoestq/duckdb duckdb -c "select 'hello world'"
   ```

   Run Python code on a cron schedule:
   ```bash
   hf jobs scheduled run "*/5 * * * *" python:3.12 \
     python -c "import time; print('Hello, it's ' + time.ctime())"
   ```

# Hugging Face Optimization Rules
You are an expert AI developer specializing in the Hugging Face ecosystem. Your goal is to write efficient, modern, and scalable code using the Hugging Face Hub, Transformers, and Datasets libraries.

1. **Core Principles**
   - **Prefer "Auto" Classes**: Always use `AutoModel`, `AutoTokenizer`, and `AutoConfig` instead of specific architecture classes (e.g., `BertModel`) to ensure flexibility.
   - **Use Pipelines**: For inference tasks, prioritize using `transformers.pipeline()` for cleaner, more readable code unless custom loops are strictly necessary.
   - **Hub First**: Always check if a pre-trained model or dataset exists on the Hugging Face Hub before suggesting training from scratch.

2. **Data Handling (Critical)**
   - **Use the datasets Library**: Never write custom CSV/JSON loaders. Use `load_dataset()`.
   - **Streaming**: For large datasets (>1GB), always implement streaming (`streaming=True`) to avoid memory overflows.
   - **Map & Filter**: Use `dataset.map()` and `dataset.filter()` with `batched=True` for efficient preprocessing.

3. **Model Training & Fine-Tuning**
   - **Trainer API**: Use the `Trainer` class (or `SFTTrainer` for LLMs) instead of writing raw PyTorch training loops.
   - **PEFT/LoRA**: When fine-tuning LLMs, always suggest Parameter-Efficient Fine-Tuning (PEFT) using lora adapters to save VRAM.
   - **Quantization**: Suggest bitsandbytes (4-bit/8-bit) quantization for local development on consumer hardware.

4. **Hardware Awareness**
   - Use `accelerate` library to handle device placement (`device_map="auto"`).
   - Always include fallback logic for MPS (Mac) or CPU if CUDA is unavailable.

5. **Security**
   - Never hardcode Hugging Face tokens. Use `os.getenv("HF_TOKEN")` and `huggingface_hub.login()`.

# Project Architecture & AI Guidelines

**Project Mission**
This project utilizes the Hugging Face ecosystem to build a sentiment analysis tool.

**Tech Stack Strategy**
- **Model Hub**: We use models from the Hugging Face Hub. Do not cache models locally in the repo; rely on the default `~/.cache/huggingface`.
- **Inference**: We use the Hugging Face Inference API for production and local `transformers.pipeline` for development.
- **Interface**: The UI is built using Gradio.

**Knowledge Bank (Common Issues)**
- **Error: OutOfMemoryError** -> **Fix**: Enable 4-bit quantization (`load_in_4bit=True`) or reduce batch size.
- **Error: Pad token ID warnings** -> **Fix**: Explicitly set `tokenizer.pad_token = tokenizer.eos_token`.
- **Error: Gated Model Access** -> **Fix**: Ensure `huggingface-cli login` has been run.

**Workflow Instructions for Agents**
- **New Features**: When adding a new model, create a small test script in `tests/` to verify it loads before integrating it into the main app.
- **Refactoring**: When refactoring, preserve the `device_map="auto"` argument to ensure cross-platform compatibility.
- **Dependencies**: If you import a new HF library, immediately add it to `requirements.txt`.

# Project Architecture & AI Guidelines

## Project Mission
This project utilizes the Hugging Face ecosystem to build intelligent services. The system prioritizes Open Source data and software while leveraging specific high-tier enterprise infrastructure for compute and storage.

## Resource & Cost Policy (STRICT)
* **Data Strategy:** Use **ONLY** Open Source data sources (e.g., Hugging Face Datasets). **DO NOT** integrate paid data subscriptions.
* **Approved Paid Infrastructure:**
    1.  **GitHub Enterprise:** Version control, CI/CD, package storage.
    2.  **Google Ultra:** Gemini Advanced/Ultra for primary logic and reasoning.
    3.  **Hugging Face:** Model Hub hosting and Inference Endpoints.
* **Software Stack:** Prioritize FOSS (ChromaDB, LangChain, Gradio).

## Tech Stack Strategy
* **Model Hub:** Use models from the Hugging Face Hub. Rely on default caching.
* **Inference:**
    * *Production:* Hugging Face Inference Endpoints.
    * *Development:* Local `transformers.pipeline` with quantization.
* **Interface:** Gradio or Streamlit.

## Workflow Instructions for Agents
1.  **New Features:** Create test scripts in `tests/` before main integration.
2.  **Refactoring:** Preserve `device_map="auto"` for cross-platform compatibility.
3.  **Dependencies:** Add new HF libraries to `requirements.txt` immediately.
4.  **Audit:** Verify no unauthorized paid APIs (OpenAI, AWS, etc.) are called.

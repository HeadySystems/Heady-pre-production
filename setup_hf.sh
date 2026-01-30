#!/bin/bash
# Install Core Hugging Face Libraries
pip install transformers datasets accelerate gradio huggingface_hub python-dotenv mcp

# Install Optimization Libraries
pip install bitsandbytes optimum

echo "----------------------------------------------------------------"
echo "Please run 'huggingface-cli login' to authenticate your machine."
echo "----------------------------------------------------------------"

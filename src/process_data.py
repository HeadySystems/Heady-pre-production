import os
import sys
import json
import time
import random
import logging
from typing import Any, Dict, List, Optional, Sequence, Union

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
DEFAULT_HF_TEXT_MODEL = os.getenv("HF_TEXT_MODEL", "gpt2")
DEFAULT_HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
HEADY_PY_WORKER_TIMEOUT_MS = int(os.getenv("HEADY_PY_WORKER_TIMEOUT_MS", "90000"))
HEADY_HF_TIMEOUT_S = int(os.getenv("HEADY_HF_TIMEOUT_S", "60"))
HEADY_HF_MAX_RETRIES = int(os.getenv("HEADY_HF_MAX_RETRIES", "2"))
HEADY_HF_USER_AGENT = os.getenv("HEADY_HF_USER_AGENT", "heady-python-worker/1.0")
HEADY_QA_MAX_QUESTION_CHARS = int(os.getenv("HEADY_QA_MAX_QUESTION_CHARS", "4000"))
HEADY_QA_MAX_CONTEXT_CHARS = int(os.getenv("HEADY_QA_MAX_CONTEXT_CHARS", "12000"))
HEADY_QA_TRUNCATE_INPUTS = os.getenv("HEADY_QA_TRUNCATE_INPUTS", "true").lower() == "true"
PROCESS_START_TIME = time.time()
SESSION = requests.Session()


def _sleep_ms(ms: int) -> None:
    time.sleep(ms / 1000.0)


def _calc_backoff_ms(attempt: int, base_ms: int = 500, max_ms: int = 5000) -> int:
    if attempt <= 0:
        return base_ms
    delay = min(max_ms, int(base_ms * (2 ** attempt)))
    jitter = int(delay * 0.2)
    return delay + int(jitter * (random.random() - 0.5))


def hf_infer(
    *,
    model: str,
    inputs: Any,
    parameters: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None,
    timeout_s: Optional[int] = None,
    max_retries: Optional[int] = None,
) -> Any:
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN is not set")

    used_timeout_s = timeout_s if timeout_s is not None else HEADY_HF_TIMEOUT_S
    used_max_retries = max_retries if max_retries is not None else HEADY_HF_MAX_RETRIES
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload: Dict[str, Any] = {"inputs": inputs}
    if parameters is not None:
        payload["parameters"] = parameters
    if options is not None:
        payload["options"] = options

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": HEADY_HF_USER_AGENT,
    }

    retry_statuses = {429, 503, 504}

    for attempt in range(used_max_retries + 1):
        try:
            resp = SESSION.post(url, json=payload, headers=headers, timeout=used_timeout_s)
        except requests.RequestException as exc:
            if attempt < used_max_retries:
                wait_ms = _calc_backoff_ms(attempt)
                logger.warning("HF request failed (%s). Retrying in %sms", exc, wait_ms)
                _sleep_ms(wait_ms)
                continue
            raise RuntimeError(f"Hugging Face request failed: {exc}") from exc

        if resp.status_code in retry_statuses and attempt < used_max_retries:
            try:
                data = resp.json()
                estimated = data.get("estimated_time")
                wait_ms = int(estimated * 1000) + 250 if isinstance(estimated, (int, float)) else _calc_backoff_ms(attempt)
            except Exception:
                wait_ms = _calc_backoff_ms(attempt)
            logger.info("HF returned %s. Retrying in %sms", resp.status_code, wait_ms)
            _sleep_ms(wait_ms)
            continue

        if resp.status_code < 200 or resp.status_code >= 300:
            try:
                data = resp.json()
            except Exception:
                data = resp.text

            message = "Hugging Face inference failed"
            if isinstance(data, dict) and isinstance(data.get("error"), str) and data["error"].strip():
                message = data["error"].strip()
            raise RuntimeError(f"{message} (status={resp.status_code})")

        return resp.json()

    raise RuntimeError("Hugging Face inference failed")


def hf_generate(
    prompt: str,
    *,
    model: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    used_model = model or DEFAULT_HF_TEXT_MODEL
    data = hf_infer(model=used_model, inputs=prompt, parameters=parameters, options=options)

    # Handle different return formats from HF API
    output = ""
    if isinstance(data, list) and data and "generated_text" in data[0]:
        output = data[0]["generated_text"]
    elif isinstance(data, dict) and "generated_text" in data:
        output = data["generated_text"]

    return {"model": used_model, "output": output, "raw": data}


def _mean_pool_2d(matrix: List[List[float]]) -> List[float]:
    if not matrix or not matrix[0]:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    pooled = []
    for c in range(cols):
        col_sum = sum(row[c] for row in matrix)
        pooled.append(col_sum / rows)
    return pooled


def _pool_feature_extraction_output(output: Any) -> Any:
    # Handle list of lists (token embeddings) -> mean pool
    if isinstance(output, list) and output and isinstance(output[0], list) and isinstance(output[0][0], list):
        # Batch of sequences
        return [_mean_pool_2d(seq) for seq in output]
    elif isinstance(output, list) and output and isinstance(output[0], list):
        # Single sequence
        return _mean_pool_2d(output)
    return output


def hf_embed(
    text: Union[str, Sequence[str]],
    *,
    model: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    used_model = model or DEFAULT_HF_EMBED_MODEL
    merged_options: Dict[str, Any] = {"wait_for_model": True}
    if isinstance(options, dict):
        merged_options.update(options)

    data = hf_infer(model=used_model, inputs=text, options=merged_options)
    embeddings = _pool_feature_extraction_output(data)
    return {"model": used_model, "embeddings": embeddings, "raw": data}


def _truncate_input(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[:limit]


def qa_interface(
    question: str,
    context: str = "",
    model: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
    max_new_tokens: int = 256,
    request_id: str = "",
) -> Dict[str, Any]:
    """QA interface for Node.js manager communication"""
    try:
        question = question or ""
        context = context or ""

        if HEADY_QA_TRUNCATE_INPUTS:
            question = _truncate_input(question, HEADY_QA_MAX_QUESTION_CHARS)
            context = _truncate_input(context, HEADY_QA_MAX_CONTEXT_CHARS)
        else:
            if len(question) > HEADY_QA_MAX_QUESTION_CHARS:
                raise ValueError("Question exceeds maximum length")
            if len(context) > HEADY_QA_MAX_CONTEXT_CHARS:
                raise ValueError("Context exceeds maximum length")

        used_model = model or DEFAULT_HF_TEXT_MODEL
        merged_parameters = {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.2,
            "return_full_text": False,
            **(parameters or {}),
        }

        prompt = f"""You are Heady Systems Q&A. Provide a clear, safe, and concise answer. Do not reveal secrets, API keys, tokens, or private data.

Context:
{context}

Question:
{question}

Answer:"""

        result = hf_generate(prompt, model=used_model, parameters=merged_parameters)
        answer = result.get("output", "")

        # Remove prompt echo if present
        if answer.startswith(prompt):
            answer = answer[len(prompt):].strip()

        return {
            "ok": True,
            "answer": answer,
            "model": used_model,
            "request_id": request_id,
            "backend": "python-hf",
        }
    except Exception as e:
        logger.error(f"QA Error: {e}")
        return {
            "ok": False,
            "error": str(e),
            "backend": "python-hf",
        }


def handle_qa_command():
    try:
        input_data = json.load(sys.stdin)
        question = input_data.get("question")
        context = input_data.get("context", "")
        model = input_data.get("model")
        parameters = input_data.get("parameters")
        max_new_tokens = input_data.get("max_new_tokens", 256)
        request_id = input_data.get("request_id", "")

        result = qa_interface(question, context, model, parameters, max_new_tokens, request_id)
        print(json.dumps(result))
        sys.exit(0)

    except Exception as e:
        error_result = {
            "ok": False,
            "error": str(e),
            "backend": "python-hf",
        }
        print(json.dumps(error_result))
        sys.exit(1)


def handle_health_check() -> None:
    """Handle health check command"""
    health_status = {
        "status": "healthy",
        "service": "heady-python-worker",
        "timestamp": int(time.time()),
        "uptime_s": int(time.time() - PROCESS_START_TIME),
        "pid": os.getpid(),
        "python_version": sys.version.split()[0],
        "hf_token_configured": bool(HF_TOKEN),
        "default_text_model": DEFAULT_HF_TEXT_MODEL,
        "default_embed_model": DEFAULT_HF_EMBED_MODEL,
        "worker_timeout_ms": HEADY_PY_WORKER_TIMEOUT_MS,
        "hf_timeout_s": HEADY_HF_TIMEOUT_S,
        "hf_max_retries": HEADY_HF_MAX_RETRIES,
    }
    print(json.dumps(health_status))
    sys.exit(0)


def main() -> None:
    """Main entry point for the Python worker"""
    # Check if we're being called with a specific command
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "qa":
            handle_qa_command()
        elif command == "health":
            handle_health_check()
        elif command == "test":
            # Placeholder for test functionality
            logger.info("Test functionality not yet implemented")
            print(json.dumps({"status": "not_implemented", "message": "Test functionality not yet implemented"}))
            sys.exit(0)
        else:
            logger.error(f"Unknown command: {command}")
            print(json.dumps({"error": f"Unknown command: {command}"}))
            sys.exit(1)

    # Default behavior: worker initialization
    logger.info("Heady Python Worker initialized")

if __name__ == "__main__":
    main()

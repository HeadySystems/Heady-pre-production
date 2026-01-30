import logging
import os
import torch
import chromadb
from typing import List, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, pipeline, BitsAndBytesConfig
from langchain_huggingface import HuggingFacePipeline
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from .utils import get_logger

logger = get_logger(__name__)

class NLPService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NLPService, cls).__new__(cls)
            cls._instance.initialized = False
            cls._instance.gemini_llm = None
            cls._instance.local_llm = None
            cls._instance.summ_pipe = None
            cls._instance.collection = None
        return cls._instance

    def initialize(self):
        if self.initialized:
            return

        logger.info("Initializing NLP Service (Optimized)...")
        self.device = 0 if torch.cuda.is_available() else -1
        self.device_name = torch.cuda.get_device_name(0) if self.device == 0 else "CPU"
        logger.info(f"Compute Device: {self.device_name}")

        try:
            # 1. Vector Store (ChromaDB) - FOSS
            # Use persistent storage
            db_path = os.path.join(os.getcwd(), "admin", "db", "chroma")
            os.makedirs(db_path, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=db_path)
            self.collection = self.chroma_client.get_or_create_collection(name="heady_knowledge_base")
            logger.info(f"ChromaDB initialized at {db_path}.")

            # 2. Local Models (Quantized if GPU)
            quantization_config = None
            if self.device == 0:
                logger.info("Configuring 4-bit quantization for local models...")
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16
                )

            # Summarization Pipeline
            # Using device_map="auto" is generally safer for accelerate handling unless explicitly on CPU
            device_arg = {"device_map": "auto"} if self.device == 0 else {"device": -1}

            self.summ_pipe = pipeline(
                "summarization",
                model="t5-small",
                model_kwargs={"quantization_config": quantization_config} if quantization_config else {},
                **device_arg
            )

            # Generation Pipeline (LangChain compatible)
            gen_pipe = pipeline(
                "text-generation",
                model="distilgpt2",
                max_new_tokens=256,
                model_kwargs={"quantization_config": quantization_config} if quantization_config else {},
                **device_arg
            )
            self.local_llm = HuggingFacePipeline(pipeline=gen_pipe)

            # 3. Google Gemini (Ultra/Advanced) - Optional
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if google_api_key:
                logger.info("Enabling Google Gemini integration...")
                self.gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

            self.initialized = True
            logger.info("NLP Service ready.")

        except Exception as e:
            logger.error(f"Failed to initialize NLP Service: {e}")
            self.initialized = False

    def summarize_text(self, text: str) -> str:
        if not self.initialized:
            self.initialize()

        try:
            # Local T5
            if self.summ_pipe:
                input_text = "summarize: " + text[:2000]
                summary = self.summ_pipe(input_text, max_length=150, min_length=30, do_sample=False)
                return summary[0]['summary_text']
            return "Summarization unavailable."
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return "Error generating summary."

    def generate_response(self, prompt: str) -> str:
        if not self.initialized:
            self.initialize()

        try:
            # Decision: Use Gemini if available
            if self.gemini_llm:
                try:
                    response = self.gemini_llm.invoke(prompt)
                    return response.content
                except Exception as ex:
                    logger.warning(f"Gemini failed, falling back to local: {ex}")

            # Local Fallback
            if self.local_llm:
                return self.local_llm.invoke(prompt)
            return "Generation unavailable."
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "Error generating response."

    def add_document_to_knowledge_base(self, doc_id: str, text: str, metadata: dict = None):
        if not self.initialized:
            self.initialize()
        try:
            if self.collection:
                existing = self.collection.get(ids=[doc_id])
                if existing['ids']:
                    self.collection.update(ids=[doc_id], documents=[text], metadatas=[metadata or {}])
                else:
                    self.collection.add(ids=[doc_id], documents=[text], metadatas=[metadata or {}])
                logger.info(f"Document {doc_id} indexed in ChromaDB.")
        except Exception as e:
            logger.error(f"Indexing error: {e}")

    def index_repository(self, root_path: str):
        """Walks the repository and indexes supported text files."""
        if not self.initialized:
            self.initialize()

        logger.info(f"Starting repository index from {root_path}...")
        count = 0
        supported_exts = {'.py', '.md', '.js', '.html', '.css', '.json', '.txt', '.yaml', '.yml'}

        for root, _, files in os.walk(root_path):
            if any(x in root for x in ['.git', '__pycache__', 'node_modules', 'venv', 'env']):
                continue

            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in supported_exts:
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # Chunking could be added here, currently full file
                            self.add_document_to_knowledge_base(
                                doc_id=path,
                                text=content,
                                metadata={"source": path, "filename": file}
                            )
                            count += 1
                    except Exception as e:
                        logger.warning(f"Failed to index {path}: {e}")

        logger.info(f"Repository indexing complete. {count} files processed.")

nlp_service = NLPService()

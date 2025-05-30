from dataclasses import dataclass 
from trading_bot.utils import load_yaml 


CONFIG=load_yaml("config/config.yaml")

@dataclass 
class DataIngestionConstants:
    PINECONE_INDEX_NAME=CONFIG.PINECONE.INDEX_NAME
    SPLITTER_CHUNK_SIZE=CONFIG.SPLITTER.CHUNK_SIZE
    SPLITTER_CHUNK_OVERLAP_SIZE=CONFIG.SPLITTER.CHUNK_OVERLAP_SIZE
    GOOGLE_EMBEDDING_MODEL_NAME=CONFIG.MODELS.EMBEDDINGS.GOOGLE
    HUGGINGFACE_EMBEDDING_MODEL_NAME=CONFIG.MODELS.EMBEDDINGS.HUGGINGFACE

@dataclass 
class ToolsConstants:
    RETRIEVER_TOP_K=CONFIG.TOOLS.RETRIEVER.TOP_K
    RETRIEVER_SCORE_THRESHOLD=CONFIG.TOOLS.RETRIEVER.SCORE_THRESHOLD
    TAVILY_MAX_RESULTS=CONFIG.TOOLS.TAVILY.MAX_RESULTS

@dataclass 
class AgentsConstants:
    GOOGLE_REASONING_MODEL_NAME=CONFIG.MODELS.REASONERS.GEMINI_FLASH
    GROQ_REASONING_MODEL_NAME=CONFIG.MODELS.REASONERS.DEEPSEEK_R1


from trading_bot.constants import (
    DataIngestionConstants,
    ToolsConstants,
    AgentsConstants
    )
from dataclasses import dataclass 


@dataclass 
class DataIngestionConfig:
    PINECONE_INDEX_NAME=str(DataIngestionConstants.PINECONE_INDEX_NAME)
    SPLITTER_CHUNK_SIZE=int(DataIngestionConstants.SPLITTER_CHUNK_SIZE)
    SPLITTER_CHUNK_OVERLAP_SIZE=int(DataIngestionConstants.SPLITTER_CHUNK_OVERLAP_SIZE)
    GOOGLE_EMBEDDING_MODEL_NAME=str(DataIngestionConstants.GOOGLE_EMBEDDING_MODEL_NAME)
    HUGGINGFACE_EMBEDDING_MODEL_NAME=str(DataIngestionConstants.HUGGINGFACE_EMBEDDING_MODEL_NAME)

@dataclass 
class ToolsConfig:
    RETRIEVER_TOP_K=int(ToolsConstants.RETRIEVER_TOP_K)
    RETRIEVER_SCORE_THRESHOLD=float(ToolsConstants.RETRIEVER_SCORE_THRESHOLD)
    TAVILY_MAX_RESULTS=int(ToolsConstants.TAVILY_MAX_RESULTS)

@dataclass 
class AgentsConfig:
    GOOGLE_REASONING_MODEL_NAME=str(AgentsConstants.GOOGLE_REASONING_MODEL_NAME)
    GROQ_REASONING_MODEL_NAME=str(AgentsConstants.GROQ_REASONING_MODEL_NAME)


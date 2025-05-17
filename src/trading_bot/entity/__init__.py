from dataclasses import dataclass


class EmbeddingsModel:
    """Embeddig class
    """

@dataclass 
class DataIngestion:
    PINECONE_INDEX_NAME:str
    SPLITTER_CHUNK_SIZE:int
    SPLITTER_CHUNK_OVERLAP_SIZE:int
    GOOGLE_EMBEDDING_MODEL_NAME:str
    HUGGINGFACE_EMBEDDING_MODEL_NAME:str

@dataclass 
class Tools:
    RETRIEVER_TOP_K:int
    RETRIEVER_SCORE_THRESHOLD:float
    TAVILY_MAX_RESULTS:int

@dataclass 
class Agents:
    GOOGLE_REASONING_MODEL_NAME:str
    GROQ_REASONING_MODEL_NAME:str


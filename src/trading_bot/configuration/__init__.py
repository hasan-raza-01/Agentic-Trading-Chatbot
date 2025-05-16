from trading_bot.constants import DataIngestionConstants
from dataclasses import dataclass 


@dataclass 
class DataIngestionConfig:
    PINECONE_INDEX_NAME=str(DataIngestionConstants.PINECONE_INDEX_NAME)
    SPLITTER_CHUNK_SIZE=int(DataIngestionConstants.SPLITTER_CHUNK_SIZE)
    SPLITTER_CHUNK_OVERLAP_SIZE=int(DataIngestionConstants.SPLITTER_CHUNK_OVERLAP_SIZE)
    GOOGLE_EMBEDDING_MODEL_NAME=str(DataIngestionConstants.GOOGLE_EMBEDDING_MODEL_NAME)
    HUGGINGFACE_EMBEDDING_MODEL_NAME=str(DataIngestionConstants.HUGGINGFACE_EMBEDDING_MODEL_NAME)



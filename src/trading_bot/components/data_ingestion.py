from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from trading_bot.utils import get_vector_store, load_embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from trading_bot.exception import CustomException
from langchain_core.documents import Document
from trading_bot.entity import DataIngestion
from trading_bot.logger import logging
from dataclasses import dataclass
from dotenv import load_dotenv
from uuid import uuid4
from typing import List
import sys, tempfile, os


@dataclass
class DataIngestionComponents:
    __data_ingestion_config:DataIngestion

    def load_documents(self, uploaded_files) -> List[Document]:
        """converts uploaded_files into langchain document object

        Args:
            uploaded_files : files uploaded

        Returns:
            List[Document]: list of document object to insert into vector store

        Note:
            uploaded_files must have .read() attribute
        """
        try:
            logging.info("In load_documents")

            documents = []
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.filename
                file_ext = os.path.splitext(file_name)[1].lower()
                suffix = file_ext if file_ext in [".pdf", ".docx"] else ".tmp"

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.file.read())
                    temp_path = temp_file.name
                    logging.info(f"created temp file for {{{file_name}}}")

                if file_ext == ".pdf":
                    loader = PyPDFLoader(temp_path)
                    documents.extend(loader.load())
                    logging.info(f"loaded temp file of {{{file_name}}} with PyPDFLoader")

                elif file_ext == ".docx":
                    loader = Docx2txtLoader(temp_path)
                    documents.extend(loader.load())
                    logging.info(f"loaded temp file of {{{file_name}}} with Docx2txtLoader")

                else:
                    print(f"Unsupported file type: {file_name}")

            logging.info("Out load_documents")
            return documents
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def store_in_vector_db(self, documents: List[Document]):
        """inserts data into vector store after performing chunking

        Args:
            documents (List[Document]): list of langchain document object to insert in vector store
        """
        try:
            logging.info("In store_in_vector_db")
            # load api keys
            load_status=load_dotenv()
            logging.info(f"load_dotenv: {{{load_status}}}")

            # create chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.__data_ingestion_config.SPLITTER_CHUNK_SIZE,
                chunk_overlap=self.__data_ingestion_config.SPLITTER_CHUNK_OVERLAP_SIZE,
                length_function=len
            )
            documents = text_splitter.split_documents(documents)
            logging.info(f"chunking completed, len(documents):{{{len(documents)}}}")

            # load embeddig model
            embeddings=load_embeddings(self.__data_ingestion_config.GOOGLE_EMBEDDING_MODEL_NAME, 
                                       self.__data_ingestion_config.HUGGINGFACE_EMBEDDING_MODEL_NAME)
            try:
                embeddings_model_name=embeddings.model
            except:
                embeddings_model_name=embeddings.model_name
            logging.info(f"loaded embeddings model {{{embeddings_model_name}}}")

            # connect with vector store
            vector_store = get_vector_store(pinecone_api_key=os.getenv("PINECONE_API_KEY"), 
                                            index_name= self.__data_ingestion_config.PINECONE_INDEX_NAME, 
                                            embeddings=embeddings)
            logging.info("loaded vector store")

            # insert data into vector store
            logging.info("data insertion initiated")
            uuids = [str(uuid4()) for _ in range(len(documents))]
            vector_store.add_documents(documents=documents, ids=uuids)
            logging.info("data insertion completed")

            logging.info("Out store_in_vector_db")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def main(self, uploaded_files) -> None:
        documents = self.load_documents(uploaded_files)
        if not documents:
            logging.warning("No valid documents found.")
            return
        self.store_in_vector_db(documents)



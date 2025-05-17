from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from trading_bot.utils import get_vector_store, load_embeddings
from langchain_community.tools import TavilySearchResults
from trading_bot.schema import RagToolSchema
from trading_bot.exception import CustomException
from trading_bot.entity import DataIngestion
from trading_bot.logger import logging
from trading_bot.entity import Tools
from dataclasses import dataclass
from langchain.tools import tool
from dotenv import load_dotenv
import os, sys


@dataclass
class ToolsComponents:
    __data_ingestion_config:DataIngestion
    __tools_config:Tools

    def __call__(self, get_tools:bool=None) -> dict[tool]:
        """post init to initalize tools

        Args:
            get_tools (bool, optional): if not provided error will be raised. Defaults to None.        

        Returns:
            dict[tool]: {
            "retriever_tool": retriever_tool,
            "tavily_tool": tavily_tool,
            "financials_tool": financials_tool
            }
        """
        try:
            if get_tools==None:
                raise ValueError("Value should only be boolean")
            
            # load api keys
            load_status=load_dotenv()
            logging.info(f"load_dotenv: {{{load_status}}}")
            
            if get_tools:
                # retriever
                @tool(args_schema=RagToolSchema)
                def retriever_tool(question):
                    """Retrieves n numbers of data from database on the basis of similarity search
                    """

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

                    retriever = vector_store.as_retriever(
                        search_type="similarity_score_threshold",
                        search_kwargs={
                            "k": self.__tools_config.RETRIEVER_TOP_K , 
                            "score_threshold": self.__tools_config.RETRIEVER_SCORE_THRESHOLD
                        }
                    )
                    return retriever.invoke(question)
                
                # tavily
                tavily_tool = TavilySearchResults(
                max_results=self.__tools_config.TAVILY_MAX_RESULTS,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True,
                )

                # polygon
                api_wrapper = PolygonAPIWrapper()
                financials_tool = PolygonFinancials(api_wrapper=api_wrapper)
                logging.info("all tools collected")

                return {
                    "retriever_tool": retriever_tool,
                    "tavily_tool": tavily_tool,
                    "financials_tool": financials_tool
                    }

        except Exception as e:
            logging.info(e)
            raise CustomException(e, sys)
        

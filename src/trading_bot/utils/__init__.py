from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from trading_bot.entity import EmbeddingsModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from trading_bot.exception import CustomException
from pinecone import ServerlessSpec, Pinecone
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pathlib import Path
from box import ConfigBox
import sys, yaml, os, json



def create_dirs(path:str)->None:
    """creates directory if path do not exists

    Args:
        path (str): directory path for creation
    """
    try:
        os.makedirs(Path(path), exist_ok=True)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_yaml(path:str)->ConfigBox:
    """reads the yaml file available in path

    Args:
        path (str): path of the yaml file

    Returns:
        ConfigBox: dict["key"] = value --------->  dict.key = value
    """
    try:
        with open(Path(path), "r") as yaml_file_obj:
            return ConfigBox(yaml.safe_load(yaml_file_obj))
    except Exception as e:
        raise CustomException(e, sys)
    

def dump_yaml(content:any, file_path:str)->None:
    """saves the yaml file with provided content

    Args:
        content (any): content for the yaml file
        path (str): path to save the file
    """
    try:
        with open(Path(file_path), "w") as file:
            yaml.safe_dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)
    
def dump_json(data:dict, path:str)->None:
    """saves the dictoanary into json file

    Args:
        data (dict): dictionary data to save in form of json
        path (str): path to save the file
    """
    try:
        # Serializing json
        json_object = json.dumps(data, indent=4)

        # Writing to sample.json
        with open(Path(path), "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_json(path:str)->dict:
    """reads the data present inside the file provided in \'path\' variable

    Args:
        path (str): path of the json file

    Returns:
        json: json of data inside file
    """
    try:
        # Opening JSON file
        with open(Path(path), 'r') as openfile:

            # Reading from json file
            json_object = json.load(openfile)
            return json_object
    except Exception as e:
        raise CustomException(e, sys)
    
def load_embeddings(google_model_name:str, huggingface_model_name:str) -> GoogleGenerativeAIEmbeddings | HuggingFaceEmbeddings:
    """loads the embedding model

    Args:
        google_model_name (str): google embeddings model name
        huggingface_model_name (str): huggingface embeddings model name

    Returns:
        GoogleGenerativeAIEmbeddings | HuggingFaceEmbeddings

    ## Note:
        First google model will be tried to load, if any error occurs huggingface model will be loaded
    """
    try:
        # load api keys
        load_dotenv()
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model=google_model_name)
            embeddings.embed_query("test query")
        except:
            embeddings = HuggingFaceEmbeddings(
                model_name = huggingface_model_name, 
                model_kwargs = {"device": "cpu"}, 
                encode_kwargs = {"normalize_embeddings": True})
            embeddings.embed_query("test query")
            
        return embeddings
    except Exception as e:
        raise CustomException(e, sys)
    
def get_vector_store(pinecone_api_key:str, index_name:str, embeddings:EmbeddingsModel) -> PineconeVectorStore:
    """creates pinecone vector store via langchain-pinecone

    Args:
        pinecone_api_key (str): api key to connect with pinecone server
        index_name (str): index name of pinecone db for data insertion
        embeddings (EmbeddingsModel): model for embeddings

    Returns:
        PineconeVectorStore: return the vector store created
    """
    try:
        pinecone_client = Pinecone(api_key=pinecone_api_key)

        if index_name not in [i.name for i in pinecone_client.list_indexes()]:
            pinecone_client.create_index(
                name=index_name,
                dimension=len(embeddings.embed_query("query for test")), 
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        index = pinecone_client.Index(index_name)

        return PineconeVectorStore(index=index, embedding=embeddings)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_reasoner(google_model_name:str, groq_model_name:str) -> ChatGoogleGenerativeAI | ChatGroq :
    """load reasoner model from google or groq

    Args:
        google_model_name (str): google reasoner model name
        groq_model_name (str): groq reasoner model name

    Raises:
        CustomException: First google model will be tried to load, if any error occurs groq model  will be tried to load if any error occurs error will be raised

    Returns:
        ChatGoogleGenerativeAI | ChatGroq
    """
    try:
        try:
            llm=ChatGoogleGenerativeAI(model=google_model_name)
            llm.invoke("hii")
        except:
            llm=ChatGroq(model=groq_model_name) 
            llm.invoke("hii")
        return llm
    except Exception as e:
        raise CustomException(e, sys)
    

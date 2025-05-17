from pydantic import BaseModel
from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages


class RagToolSchema(BaseModel):
    question:str 
    
class QuestionRequest(BaseModel):
    question: str

class State(TypedDict):
    messages: Annotated[list, add_messages]


from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from trading_bot.exception import CustomException
from langgraph.graph import StateGraph, START
from trading_bot.utils import load_reasoner
from trading_bot.logger import logging
from langchain_core.tools import tool
from trading_bot.entity import Agents
from trading_bot.schema import State
from typing import List
import sys 



class AgentsComponents:
    
    def __init__(self, __Agents_config:Agents, __tools:List[tool]):
        try:
            self.__Agents_config=__Agents_config
            self.__tools=__tools
            self.llm=load_reasoner(self.__Agents_config.GOOGLE_REASONING_MODEL_NAME, self.__Agents_config.GROQ_REASONING_MODEL_NAME)
            
            graph_builder=StateGraph(State)
        
            graph_builder.add_node("chatbot", self.__chatbot_node)
            
            tool_node=ToolNode(tools=self.__tools)
            graph_builder.add_node("tools", tool_node)
            
            graph_builder.add_conditional_edges("chatbot", tools_condition)
            graph_builder.add_edge("tools", "chatbot")
            graph_builder.add_edge(START, "chatbot")
            
            self.__graph=graph_builder.compile() 
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    

    def __chatbot_node(self, state:State) -> dict:
        """node for llm chat

        Args:
            state (State): should have attribute/key named as messages, messages should be list

        Returns:
            dict: {"messages": [output of llm]}
        """
        try:
            self.llm_with_tools=self.llm.bind_tools(self.__tools)
            result=self.llm_with_tools.invoke(state["messages"])

            return {"messages": [result]}
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)

    def get_graph(self) -> StateGraph:
        """builds agentic graph/workflow

        Returns:
            StateGraph: graph/workflow
        """
        return self.__graph
    

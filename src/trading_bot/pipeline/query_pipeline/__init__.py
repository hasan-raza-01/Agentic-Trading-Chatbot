from trading_bot.configuration import (
    DataIngestionConfig,
    AgentsConfig
)
from trading_bot.components.tools import ToolsComponents
from trading_bot.components.agents import AgentsComponents
from trading_bot.configuration import ToolsConfig
from trading_bot.schema import State


class QueryPipeline:

    def __init__(self) -> None:
        # tools
        tools_obj=ToolsComponents(DataIngestionConfig, ToolsConfig)
        tools_dict=tools_obj(get_tools=True)
        tools=[
            tools_dict["retriever_tool"], 
            tools_dict["tavily_tool"], 
            tools_dict["financials_tool"]
        ]

        # workflow
        workflow=AgentsComponents(AgentsConfig, tools)
        self.graph=workflow.get_graph()

    def run(self, messages:State) -> State:
        return self.graph.invoke(messages)


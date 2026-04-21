from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from model.factory import chat_model
from agent.tools.agent_tools import (
    rag_summarize, get_weather, get_user_location,
    get_user_id, get_current_month,
    fetch_external_data, fill_context_for_report
)


class ReactAgent:
    def __init__(self):
        self.llm = chat_model  # ⚠️ 不加()

        self.tools = [
            Tool(name="rag_summarize", func=rag_summarize, description="总结知识库"),
            Tool(name="get_weather", func=get_weather, description="获取天气"),
            Tool(name="get_user_location", func=get_user_location, description="获取用户位置"),
            Tool(name="get_user_id", func=get_user_id, description="获取用户ID"),
            Tool(name="get_current_month", func=get_current_month, description="获取当前月份"),
            Tool(name="fetch_external_data", func=fetch_external_data, description="外部数据"),
            Tool(name="fill_context_for_report", func=fill_context_for_report, description="报告补充"),
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def execute(self, query: str):
        return self.agent.run(query)


if __name__ == "__main__":
    agent = ReactAgent()
    result = agent.execute("给我生成我的使用报告")
    print(result)
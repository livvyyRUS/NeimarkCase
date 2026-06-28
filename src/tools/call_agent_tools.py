from typing import List, Tuple
from langchain_core.tools import tool
from src.agents import get_agent_dict, BaseAgent

agent_dict = get_agent_dict()


class CallAgentTools:
    @staticmethod
    @tool
    def call_agent(agent: str, message: str):
        """
        Вызывает заданного агента для выполнения задачи или получения информации.

        Этот инструмент использует предопределенный словарь агентов 
        для инициализации нужного агента и выполняет его основную функцию.

        :param agent: Название агента, который необходимо вызвать (ключ в get_agent_dict()).
        :type agent: str
        :param message: Сообщение или запрос для агента.
        :type message: str
        :return: Ответ от вызванного агента.
        :rtype: str
        """
        print("tool execute: call_agent")
        agent: BaseAgent = agent_dict.get(agent)
        answer = agent.run_agent(message)
        return answer
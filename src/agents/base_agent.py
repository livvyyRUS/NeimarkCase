from src.llm import get_llm
from src.logger import logger
from langchain_core.tools import BaseTool
from langchain.agents import create_agent
from pathlib import Path
import traceback

class BaseAgent:
    def __init__(
        self, 
        base_url: str, 
        model_name: str, 
        api_key: str,
        tools: list[BaseTool], # Moved mandatory argument up
        agent_type: str # System prompt is optional and placed last
    ):
        """
        Initialize the BaseAgent with the provided base URL, model name, and API key.

        Args:
            base_url (str): The base URL of the language model API.
            model_name (str): The name of the language model to use.
            api_key (str): The API key for authentication.
            tools: list[BaseTool]: List of tools available to the agent.
            system_prompt (str | None, optional): System instruction for the agent behavior. Defaults to None.
        """
        # Attributes initialization and setup order is crucial
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.agent_type = agent_type
        self.system_prompt = self.get_system_prompt()
        self.tools = tools 
        self.history: list[dict] = [] # Internal history for conversation memory

        # Get the LLM instance first (Requires success in get_llm)
        self.llm = get_llm(self.base_url, self.model_name, self.api_key)

        # Create the agent using the initialized components
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools
        )
        
    
    def get_system_prompt(self):
        file_path = Path(f"prompts/{self.agent_type}.md")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        
        with open(f"prompts/{self.agent_type}.md", "r", encoding="utf8") as file:
            system_prompt = file.read().strip()
        return system_prompt
        

    def run_agent(self, input: str) -> dict | str:
        """
        Runs the agent with a given input. Automatically manages and updates conversational history.

        The system prompt is applied once (stored in history) and persists across turns.
        The results of this run (both user input and assistant response) are stored in self.history.

        Args:
            input (str): The user's initial query or input.

        Returns:
            dict | str: A dictionary containing the agent's final response under the 'output' key, 
                        or an error string if execution fails.
        """
        logger.info(f"Вызван агент {self.agent_type}")
        
        # 1. Инициализируем историю, если она пуста, и добавляем system_prompt только один раз
        if not self.history:
            if self.system_prompt:
                self.history.append({"role": "system", "content": self.system_prompt})

        # 2. Формируем список сообщений для вызова агента
        messages = []
        for msg in self.history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append(msg)

        # 3. Добавляем текущий пользовательский ввод
        user_message = {"role": "user", "content": input}
        messages.append(user_message)

        try:
            # 4. ВЫЗЫВАЕМ АГЕНТА С ПРАВИЛЬНЫМ ФОРМАТОМ ВХОДНЫХ ДАННЫХ
            # LangGraph ожидает словарь с ключом 'messages'[reference:0]
            response = self.agent.invoke({"messages": messages})
            
            # 5. Извлекаем ответ ассистента из результата
            # В LangGraph результат содержит ключ 'messages' со списком всех сообщений[reference:1]
            # Берём последнее сообщение от ассистента
            if "messages" in response and response["messages"]:
                last_message = response["messages"][-1]
                output = last_message.content if hasattr(last_message, "content") else str(last_message)
            else:
                output = str(response)

            # 6. Обновляем историю: добавляем и запрос пользователя, и ответ ассистента
            self.history.append(user_message)
            self.history.append({"role": "assistant", "content": output})

            return {"output": output}

        except Exception as e:
            a = traceback.format_exception(e)
            
            error_msg = f"Agent execution failed: {e}"
            logger.error(f"Agent failed: {error_msg}")
            return {"error": error_msg}
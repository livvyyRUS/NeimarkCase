from src.llm import get_llm
from langchain_core.tools import BaseTool
from langchain.agents import create_agent

class BaseAgent:
    def __init__(
        self, 
        base_url: str, 
        model_name: str, 
        api_key: str,
        tools: list[BaseTool], # Moved mandatory argument up
        system_prompt: str | None = None # System prompt is optional and placed last
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
        self.system_prompt = system_prompt if system_prompt else None # Store prompt
        self.tools = tools 
        self.history: list[dict] = [] # Internal history for conversation memory

        # Get the LLM instance first (Requires success in get_llm)
        self.llm = get_llm(self.base_url, self.model_name, self.api_key)

        # Create the agent using the initialized components
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools
        )


    def run_agent(self, input: str) -> dict | str:
        """
        Runs the agent with a given input. Automatically manages and updates conversational history.

        The system prompt is applied before running the interaction. The results of this run 
        will be stored in self.history.

        Args:
            input (str): The user's initial query or input.

        Returns:
            dict | str: A dictionary containing the agent's final response under the 'output' key, 
                         or an error string if execution fails.
        """
        messages = []
        
        # Add System Prompt if available
        if self.system_prompt:
             messages.append({"role": "system", "content": self.system_prompt})

        # Append conversation history up to the current turn
        for msg in self.history:
            if isinstance(msg, dict): # Safety check for dict structure
                messages.append(msg)

        # Add the current user input
        user_message = {"role": "user", "content": input}
        messages.append(user_message)

        try:
            # Invoke the agent with all gathered messages (including history, system prompt, and new input)
            response = self.agent.invoke(messages)
            output = response.get('output', str(response)) 
            result_data = {"output": output}
            self.history.append({"role": "user", "content": input}) # Store user message for next turn's history
            return result_data

        except Exception as e:
            error_msg = f"Agent execution failed: {e}"
            print(f"Agent failed: {error_msg}")
            # Do not update history on failure
            return {"error": error_msg}
from .base_agent import BaseAgent
from src.tools.call_agent_tools import CallAgentTool

class OrchestratorAgent(BaseAgent):
    def __init__(self, base_url, model_name, api_key, temperature):
        tools = [
            CallAgentTool.call_agent
        ]
        
        super().__init__(base_url, model_name, api_key, temperature, tools, "orchestrator")
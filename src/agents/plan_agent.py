from .base_agent import BaseAgent
from src.tools import list_files, write_file, read_file, execute_command

class PlanAgent(BaseAgent):
    def __init__(self, base_url, model_name, api_key):
        tools = [
            list_files,
            write_file,
            read_file
        ]
        
        super().__init__(base_url, model_name, api_key, tools, "plan")
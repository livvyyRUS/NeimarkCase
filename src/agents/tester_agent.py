from .base_agent import BaseAgent
from src.tools import list_files, write_file, read_file, delete_file, execute_command

class TesterAgent(BaseAgent):
    def __init__(self, base_url, model_name, api_key, temperature):
        tools = [
            list_files,
            write_file,
            delete_file,
            read_file,
            execute_command
        ]
        
        super().__init__(base_url, model_name, api_key, temperature, tools, "tester")
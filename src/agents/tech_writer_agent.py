from .base_agent import BaseAgent
from src.tools import list_files, write_file, read_file, delete_file, execute_command

class TechWriterAgent(BaseAgent):
    def __init__(self, base_url, model_name, api_key, temperature):
        tools = [
            list_files,
            write_file,
            delete_file,
            read_file
        ]
        
        super().__init__(base_url, model_name, api_key, temperature, tools, "tech_writer")
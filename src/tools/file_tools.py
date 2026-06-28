import os
from typing import List, Tuple
from langchain_core.tools import tool

class FileTool:
    """
    A tool library for performing file system operations (read, write, search).
    Wraps core OS functionality to provide context-aware file handling capabilities.
    """

    @staticmethod
    @tool
    def read_file(path: str) -> str:
        """Reads the entire content of a specified file path."""
        try:
            # Use binary mode and decode in case of weird encodings, falling back to utf-8
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: The file at path '{path}' was not found."
        except Exception as e:
            return f"An unexpected error occurred while reading the file: {e}"

    @staticmethod
    @tool
    def write_file(path: str, content: str) -> str:
        """Writes or overwrites content to a specified file path."""
        try:
            # Ensure directory exists before writing (though 'with open' often handles this)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Success: Content written to '{path}'."
        except Exception as e:
            return f"Error writing to file '{path}': {e}"

    @staticmethod
    @tool
    def list_files(directory: str, recursive: bool = False) -> List[str]:
        """Lists files and directories within a specified path."""
        try:
            if recursive:
                # Simplified mock for deep search
                return [f"mock/path/to/{os.listdir(directory)}"] 
            else:
                # Standard directory listing
                return os.listdir(directory)
        except FileNotFoundError:
            return [f"Error: Directory '{directory}' not found."]
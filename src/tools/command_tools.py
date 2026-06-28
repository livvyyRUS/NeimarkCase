import subprocess
from typing import List, Tuple
from src.logger import logger
from langchain_core.tools import tool

class CommandTool:
    """
    A tool wrapper for executing shell commands in the operating system environment.
    This tool provides abstraction over direct CLI execution, suitable for
    integration into an agentic workflow (e.g., LangChain Tool definition).
    """

    @staticmethod
    @tool
    def execute_command(command: str) -> str:
        """
        Executes a shell command and returns the combined standard output and error stream.

        Args:
            command: The full CLI command string to execute (e.g., 'pip install requests').

        Returns:
            A string containing the execution result, or an error message if failed.
        """
        logger.info(f"Tool execute: execute_command | Executing command: {command}")
        try:
            # Using subprocess.run for reliable capture of stdout and stderr
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=True, # Raise CalledProcessError on non-zero exit code
                encoding='utf-8',
                timeout=30
            )
            # Combine stdout and stderr for a comprehensive result
            return f"Command executed successfully. STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        except subprocess.CalledProcessError as e:
            return (f"Execution Failed with Exit Code {e.returncode}.\n"
                    f"STDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            return "Execution Failed: Command timed out."
        except Exception as e:
            return f"An unexpected error occurred during command execution: {e}"
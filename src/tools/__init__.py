from .file_tools import FileTool
from .command_tools import CommandTool

# Initialize a dictionary or list of tools that can be passed to the agent framework.
AVAILABLE_TOOLS = [
    FileTool.list_files,
    FileTool.read_file,
    FileTool.write_file,
    CommandTool.execute_command,
]
from .file_tools import FileTool
from .command_tools import CommandTool

list_files = FileTool.list_files
read_file = FileTool.read_file
write_file = FileTool.write_file
delete_file = FileTool.delete_file

execute_command = CommandTool.execute_command
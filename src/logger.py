import sys
from loguru import logger

# Удаляем стандартный вывод в консоль
logger.remove()

# Добавляем свой формат с цветами
logger.add(
    sys.stderr, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

logger.add(
    "logs/app_{time:YYYY-MM-DD_HH-mm-ss}.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
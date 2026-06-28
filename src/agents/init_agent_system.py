from src.logger import logger

from src.settings import Settings
from pydantic.alias_generators import to_pascal
import importlib
from typing import Dict, Any

def initialize_agents() -> Dict[str, Any]:
    """
    Инициализирует словарь агентов на основе настроек из settings.json.
    Эта функция должна вызываться явно и возвращает словарь агентов.
    """
    # Чтение файла настроек предполагает, что он находится относительно рабочего каталога проекта.
    try:
        with open("settings.json", "r", encoding="utf8") as file:
            json_settings = file.read().strip()
            
        settings = Settings.model_validate_json(json_settings)
    except FileNotFoundError:
        logger.error("Error: settings.json not found in the current working directory.")
        return {}

    agent_dict = {}

    for model in settings.models:
        if model.name == "orchestrator":
            continue
        
        try:
            # Динамически импортируем модуль агента (например, .plan_agent)
            module = importlib.import_module(f".{model.name}_agent", package=__package__)
            
            class_name = to_pascal(model.name)
            
            # Получаем класс агента
            AgentClass = getattr(module, f"{class_name}Agent")
            
            # Создаем экземпляр агента
            agent_dict[model.name] = AgentClass(
                base_url=model.base_url,
                model_name=model.model_name,
                api_key=model.api_key, 
                temperature=model.temperature
            )
        except AttributeError:
            logger.warning(f"Warning: Could not find {class_name}Agent in module {model.name}. Skipping this agent.")
        except Exception as e:
            logger.error(f"Error initializing agent for {model.name}: {e}")

    return agent_dict


def get_agent_dict() -> Dict[str, Any]:
    """
    Предоставляет доступ к инициализированному словарю агентов с использованием ленивой инициализации (Singleton pattern).
    При первом вызове запускает initialize_agents().
    """
    # Используем атрибут функции для кеширования результата
    if not hasattr(get_agent_dict, "cache"):
        logger.info("Initializing agent dictionary for the first time...")
        get_agent_dict.cache = initialize_agents()
    return get_agent_dict.cache
# Импортируем только функции, чтобы избежать раннего выполнения логики инициализации.
# Агенты должны быть получены через функцию get_agents() для устранения циклической зависимости.
from .init_agent_system import initialize_agents, get_agent_dict

from .base_agent import BaseAgent
from src.logger import logger

from src.agents.orchestrator_agent import OrchestratorAgent
from src.settings import Settings

with open("settings.json", "r", encoding="utf8") as file:
    json_settings = file.read().strip()
    
settings = Settings.model_validate_json(json_settings)

agent = OrchestratorAgent(
    base_url=settings.models[0].base_url, 
    model_name=settings.models[0].model_name,
    api_key=settings.models[0].api_key,
    temperature=settings.models[0].temperature,
)

query = input("Введите запрос: ")

while query != "exit":
    answer = agent.run_agent(query)
    logger.info(answer)
    json.answer()
    query = input("Введите запрос: ")

# from src.tui import EventApp

# app = EventApp()
# app.run()
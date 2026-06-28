from src.agents.orchestrator_agent import OrchestratorAgent
from src.settings import Settings

with open("settings.json", "r", encoding="utf8") as file:
    json_settings = file.read().strip()
    
settings = Settings.model_validate_json(json_settings)

agent = OrchestratorAgent(
    base_url=settings.models[0].base_url, 
    model_name=settings.models[0].model_name,
    api_key=settings.models[0].api_key
)

answer = agent.run_agent("В папке output создай проект 'калькулятор' на python")
print(answer)
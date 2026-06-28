from pydantic import BaseModel

class Model(BaseModel):
    name: str
    base_url: str
    model_name: str
    api_key: str
    temperature: float
    
class Settings(BaseModel):
    models: list[Model]
    

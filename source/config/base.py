from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    EMBEDDING_BASE_URL: str
    LLM_BASE_URL: str
    LLM_API_KEY: str

    class Config:
        env_file = '.env'
        
settings = Settings()
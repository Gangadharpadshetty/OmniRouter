from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    OPENROUTER_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_PROVIDER: str = "openrouter"  # openrouter or openai
    LLM_MODEL: str = "openai/gpt-3.5-turbo"

    class Config:
        env_file = ".env"

settings = Settings()

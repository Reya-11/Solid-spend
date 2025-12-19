from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # For direct PostgreSQL connection
    DATABASE_URL: str

    # For external currency conversion API
    EXCHANGE_RATE_API_KEY: str = ""
    
    # model_config replaces the old `class Config`
    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_base_url: str
    ollama_visison_model: str
    ollam_embed_model: str
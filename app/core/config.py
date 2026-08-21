from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_base_url: str
    ollama_vision_model: str
    ollam_embed_model: str
    
    
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    
    app_env: str = "development"
    image_corpus_dir: str = "data/images"
    
    app_env: str = "development"
    image_corpus_dir: str = "data/images"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
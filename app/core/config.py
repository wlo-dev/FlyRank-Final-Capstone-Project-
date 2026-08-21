from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Central configuration for the app, loaded from .env.
    pydantic-settings reads .env and validates each value against
    the type hints below. If something is missing or the wrong
    type, the app fails immediately at startup with a clear error
    instead of crashing later, deep inside some unrelated function.
    """
    
    #-------Ollama-----
    # Required: no app startup without these, since the vision
    # pipeline can't function without knowing where Ollama lives.
    ollama_base_url: str
    ollama_vision_model: str
    ollam_embed_model: str
    
    # --- Postgres ---
    # Required: a missing/wrong DB credential should fail loudly
    # at startup, not silently break a query three files later.
    postgres_host: str
    postgres_port: int # cast from .env string to a real int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    
    app_env: str = "development"
    image_corpus_dir: str = "data/images"
    
    app_env: str = "development"
    image_corpus_dir: str = "data/images"
    
      # Tells pydantic-settings where the .env file is and how to read it.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # so ollama_base_url matches OLLAMA_BASE_URL
    )
    
    @property
    def database_url(self) -> str:
         # Builds the full Postgres connection string once, here,
        # so nothing else in the app has to assemble it by hand.
    
        return(
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        
        
# Create ONE Settings instance when this module is first imported.
# Every other file in the app will import `settings` from here rather
# than creating its own Settings() — this guarantees .env is read once
# and every part of the app sees the exact same values.
settings = Settings()
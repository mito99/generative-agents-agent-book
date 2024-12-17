import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "agent-book"

    # for Application
    google_model: str = "gemini-2.0-flash-exp"
    google_model_flash: str = "gemini-1.5-flash-latest"
    google_embedding_model: str = "models/text-embedding-004"
    temperature: float = 0.0
    default_reflection_db_path: str = "tmp/reflection_db.json"

    def __init__(self, **values):
        super().__init__(**values)
        self._set_env_variables()

    def _set_env_variables(self):
        for key in self.__annotations__.keys():
            if key.isupper():
                os.environ[key] = getattr(self, key)

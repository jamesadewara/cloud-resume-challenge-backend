from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URL: str = Field(default="mongodb://localhost:27017/resume_db")
    APP_NAME: str = Field(default="James Adewara Resume API")
    DB_NAME: str = Field(default="resume_db")
    # Added 'null' to support local file:// development
    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173,http://localhost:8000,null")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

settings = Settings()

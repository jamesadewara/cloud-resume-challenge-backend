from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env file."""
    
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017/resume_db",
        description="MongoDB connection string with database name",
    )
    
    APP_NAME: str = Field(
        default="James Adewara Resume API",
        description="Name of the application",
    )
    
    DB_NAME: str = Field(
        default="resume_db",
        description="MongoDB database name",
    )

    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:8000",
        description="Comma-separated list of allowed CORS origins",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

settings = Settings()

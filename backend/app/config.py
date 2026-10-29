from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # App
    app_name: str = "PlacePilot API"
    app_version: str = "1.0.0"
    debug: bool = True
    app_env: str = "development"

    # Database — defaults to SQLite so the app runs without PostgreSQL
    # Set DATABASE_URL=postgresql://... in .env for PostgreSQL
    database_url: str = "sqlite:///./placepilot.db"

    # JWT
    jwt_secret_key: str = "placepilot-dev-secret-key-2024"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # CORS
    allowed_origins: str = (
        "http://localhost:3000,http://localhost:5173,https://place-pilot-3mft.vercel.app"
    )

    # GenAI
    gemini_api_key: str = ""
    genai_mode: str = "demo"  # "demo" or "real"

    # Sandboxed Code Execution (Judge0)
    judge0_api_url: str = "https://ce.judge0.com"
    judge0_api_key: str = ""
    judge0_api_host: str = "judge0-ce.p.rapidapi.com"

    # ML
    ml_model_path: str = "./app/ml/models/random_forest_model.pkl"
    shap_mode: str = "real"

    # File Upload
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 10

    # Admin
    admin_default_email: str = "admin@placepilot.edu"
    admin_default_password: str = "Admin@123!"

    @property
    def allowed_origins_list(self) -> list[str]:
        default_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "https://place-pilot-3mft.vercel.app",
        ]
        origins: list[str] = []
        raw_list = [o.strip().rstrip("/") for o in self.allowed_origins.split(",") if o.strip()]
        for origin in default_origins + raw_list:
            if origin and origin not in origins:
                origins.append(origin)
        return origins

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

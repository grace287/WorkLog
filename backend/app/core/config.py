# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    환경 변수 관리
    .env 파일에서 자동으로 읽어옴
    """
    
    # Project
    PROJECT_NAME: str = "WorkLog"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database (alembic 등에서 필수)
    DATABASE_URL: str

    # Redis (기본값: 로컬, alembic 시 불필요)
    REDIS_URL: str = "redis://localhost:6379"

    # Security (기본값: 개발용, 운영에서는 반드시 .env에 설정)
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS (프론트엔드 연결)
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js 기본 포트
        "http://127.0.0.1:3000",
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


# 싱글톤 인스턴스
settings = Settings()
"""
核心配置模块
============
使用 pydantic-settings 从环境变量/.env文件加载配置。
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import structlog


class Settings(BaseSettings):
    """应用全局配置"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # --- 应用 ---
    APP_NAME: str = "金钥匙智知"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # --- 服务 ---
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # --- 数据库 ---
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/app.db"
    
    # --- Redis ---
    REDIS_URL: str = ""
    
    # --- JWT ---
    SECRET_KEY: str = "change-me-to-a-random-string-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # --- LLM ---
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"
    
    # --- Embedding ---
    EMBEDDING_API_KEY: str = ""
    EMBEDDING_BASE_URL: str = "https://api.openai.com/v1"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # --- 向量数据库 ---
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"
    
    # --- 文件存储 ---
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 50
    
    # --- 租户配额 ---
    FREE_MAX_DOCUMENTS: int = 10
    FREE_MAX_STORAGE_MB: int = 100
    FREE_MAX_API_CALLS_PER_DAY: int = 100
    
    # --- CORS ---
    CORS_ORIGINS: List[str] = ["*"]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # --- 计算属性 ---
    @property
    def UPLOAD_PATH(self) -> Path:
        path = Path(self.UPLOAD_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def DATA_PATH(self) -> Path:
        path = Path("./data")
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"
    
    @property
    def logger(self):
        return structlog.get_logger()


# 全局单例
settings = Settings()

from pydantic_settings import BaseSettings

class ClientSettings(BaseSettings):
    REDIS_HOST : str = "localhost"
    REDIS_PORT : int = 6379
    REDIS_DB : int = 0
    REDIS_PASSWORD : str | None = None
    REDIS_TLS : bool | None = None

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = True
    MINIO_BUCKET: str = "textshr"

    class Config:
        env_file = ".env"

settings = ClientSettings()
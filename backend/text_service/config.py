from pydantic_settings import BaseSettings

class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class MinioSettings(BaseSettings):
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool
    MINIO_BUCKET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# class AppSettings(BaseSettings):  # ⚠️ ДОДАЙ ЦЕ
#     SIZE_THRESHOLD: int = 10240  # 10 KB в байтах
#
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"
#         extra = "ignore"
#

redis_settings = RedisSettings()
minio_settings = MinioSettings()
# app_settings = AppSettings()  # ⚠️ ДОДАЙ ЦЕ
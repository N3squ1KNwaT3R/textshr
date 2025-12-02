import io
import asyncio
import logging
from typing import Optional

from .minio_factory import create_minio_client

logger = logging.getLogger(__name__)

class MinioClient:
    def __init__(self):
        self.minio_factory = create_minio_client()


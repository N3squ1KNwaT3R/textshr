import logging
from minio import Minio
from io import BytesIO
from clients.minio_factory import create_minio_client
from config import minio_settings

logger = logging.getLogger(__name__)


class MinioClient:
    def __init__(self):
        self.bucket = minio_settings.MINIO_BUCKET
        self.client: Minio = create_minio_client()

    def set(self, object_name: str, data: bytes):
        try:
            data_stream = BytesIO(data)
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=object_name,
                data=data_stream,
                length=len(data)
            )
            logger.info(f"UPLOAD {object_name} size={len(data)}")
        except Exception as e:
            raise Exception(f"Minio UPLOAD error object_name={object_name}: {e}")

    def get(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()

            logger.info(f"GET {object_name}")
            return data
        except Exception as e:
            raise Exception(f"Minio GET error object_name={object_name}: {e}")

    def delete(self, object_name: str) -> bool:
        try:
            exist = self._exists(object_name)
            if exist:
                self.client.remove_object(self.bucket, object_name)
                logger.info(f"DELETE {object_name}")
                return True
            return False

        except Exception as e:
            raise Exception(f"Minio DELETE error object_name={object_name}: {e}")

    def update(self, object_name: str, data: bytes) -> bool:
        try:
            exist = self._exists(object_name)
            if exist:
                self.set(object_name, data)
                logger.info(f"UPDATE {object_name}")
                return True
            return False

        except Exception as e:
            raise Exception(f"Minio UPDATE error object_name={object_name}: {e}")

    def _exists(self, object_name: str) -> bool:
        try:
            stat = self.client.stat_object(self.bucket, object_name)
            return stat is not None
        except Exception as e:
            logger.debug(f"Object {object_name} not found: {e}")
            return False


minio_client = MinioClient()

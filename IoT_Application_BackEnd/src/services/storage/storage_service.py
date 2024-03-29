import uuid
from services.storage.base_storage_manager import BaseS3Manager


class StorageService(BaseS3Manager):
    bucket_name = None

    def __init__(self, bucket_name: str):
        super().__init__()
        self.bucket_name = bucket_name

    def create_zip_and_upload_code(self, code: dict) -> str:
        guid = str(uuid.uuid4())
        zip_name = f'{guid}.zip'
        tags = {
            'Key': 'file-type',
            'Value': 'zip'
        }
        response = self.create_and_upload_zip(self.bucket_name, code, zip_name, tags)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("Error creating zip and uploading to S3")
        return zip_name

    def create_url(self, zip_name: str) -> str:
        response = self.get_presigned_url(self.bucket_name, zip_name)
        if not response:
            raise Exception("Error creating URL")
        return response

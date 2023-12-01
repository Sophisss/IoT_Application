from services.storage.base_storage_manager import BaseS3Manager


class StorageService(BaseS3Manager):
    bucket_name = None

    def __init__(self, bucket_name: str):
        BaseS3Manager.__init__(self)
        self.bucket_name = bucket_name

    def create_zip_and_upload_code(self, code: dict):
        response = self.create_and_upload_zip(self.bucket_name, code, 'code.zip')
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("Error creating zip and uploading to S3")

    def create_url(self):
        response = self.get_presigned_url(self.bucket_name, 'code.zip')
        if not response:
            raise Exception("Error creating URL")
        return response

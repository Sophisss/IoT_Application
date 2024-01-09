import zipfile
from typing import Optional

import boto3
from io import BytesIO
from services.response.base_aws_service import BaseAWSService


class BaseS3Manager(BaseAWSService):
    s3_client = None

    def __init__(self):
        super().__init__("StorageService")
        self.s3_client = boto3.client('s3')

    def get_object(self, bucket_name: str, key: str) -> dict:
        self.__validate_bucket_name(bucket_name)
        return self.s3_client.get_object(Bucket=bucket_name, Key=key)

    def put_object(self, bucket_name: str, key: str, body: bytes, tags: Optional[dict] = None) -> dict:
        self.__validate_bucket_name(bucket_name)
        if not key or not isinstance(key, str):
            raise Exception("key is mandatory and it must be a string")
        if not body:
            raise Exception("body is mandatory")

        if not tags:
            response = self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
        else:
            response = self.s3_client.put_object_tagging(Bucket=bucket_name, Key=key, Body=body, Tagging=f'{",".join([f"{key}={value}" for key, value in tags.items()])}')

        BaseAWSService.validate_aws_response(self, response, "put_object")
        return response

    def create_and_upload_zip(self, bucket_name: str, code: dict, zip_key: str) -> dict:
        self.__validate_bucket_name(bucket_name)
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, file_content in code.items():
                zip_file.writestr(file_name, file_content)

        zip_buffer.seek(0)
        tags = {'file-type': 'zip'}
        return self.put_object(bucket_name, zip_key, zip_buffer.getvalue(), tags)

    def get_presigned_url(self, bucket_name: str, zip_key: str) -> str:
        self.__validate_bucket_name(bucket_name)
        if not zip_key or not isinstance(zip_key, str):
            raise Exception("zip_key is mandatory and it must be a string")

        return self.s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': zip_key},
                                                     ExpiresIn=3600)

    @staticmethod
    def __validate_bucket_name(bucket_name: str):
        if not bucket_name or not isinstance(bucket_name, str):
            raise Exception("bucket_name is mandatory and it must be a string")

import json
import os
import zipfile
import boto3
from io import BytesIO
from typing import Optional
from botocore.exceptions import ClientError
from services.storage import http_status_code
from services.storage.base_aws_service import BaseAWSService


class Storage(BaseAWSService):
    BUCKET_NAME = os.environ['BUCKET_NAME']
    s3_client = None

    def __init__(self):
        BaseAWSService.__init__(self, "StorageService")  # base class constructor
        self.s3_client = boto3.client('s3')

    def put_object_to_s3(self, codes: dict) -> dict:
        return self.__put_object_to_s3(codes)

    def create_zip(self, keys):
        self.__create_zip(keys)

    def create_url(self) -> dict:
        return self.__create_url()

    # region utility methods

    def __put_object_to_s3(self, codes: dict) -> dict:
        """
        This function upload objects to S3.
        :param codes: the codes generated to upload.
        :return: Standardized response.
        """
        for key, value in codes.items():
            response = self.get_s3_client().put_object(Bucket=self.get_bucket_name(), Key=key, Body=value)

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return http_status_code.internal_server_error(json_body={"error": "Error uploading object to S3"})

        return http_status_code.ok(json_body={"message": "Object uploaded successfully"})

    def __create_zip(self, keys):
        """
        This function create a zip file with the objects in the list.
        :param keys: List of folders.
        :exception ClientError: Error getting the object.
        """
        bucket_name = self.get_bucket_name()
        with BytesIO() as archive:
            with zipfile.ZipFile(archive, 'w') as zip_file:
                try:
                    for obj in self.__list_objects(keys):
                        response = self.__get_s3_object(obj['Key'])

                        if response['statusCode'] == 200:
                            file_body = response['body']['data']['Body'].read()

                        zip_file.writestr(obj['Key'], file_body)
                except ClientError as error:
                    return http_status_code.internal_server_error(json_body={"error": error})

            archive.seek(0)
            self.get_s3_client().upload_fileobj(archive, bucket_name, 'code.zip')

    def __list_objects(self, keys) -> list:
        """
        This function list all the objects in a folder.
        :param keys: List of folders.
        :return: List of objects.
        """
        objects = []
        try:
            for folder_name in keys:
                response = self.get_s3_client().list_objects_v2(Bucket=self.get_bucket_name(), Prefix=folder_name)
                if 'Contents' in response:
                    objects.extend(response['Contents'])

            return objects
        except ClientError as error:
            return http_status_code.internal_server_error(json_body={"error": error})

    def __create_url(self, zip_key='code.zip') -> dict:
        """
        This function create a presigned url.
        :param zip_key: The key of the object.
        :return: Standardized response.
        """
        url = self.__generate_presigned_url(zip_key)

        if url:
            return http_status_code.ok(json_body=json.dumps({"message": "Url created successfully", "url": url}))
        else:
            return http_status_code.internal_server_error(json_body={"error": "Error creating url"})

    def __generate_presigned_url(self, zip_key: str) -> Optional:
        """
        This function generate a presigned url.
        :param zip_key: The key of the object.
        :return: Presigned url if success, None otherwise.
        """
        url = self.get_s3_client().generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.get_bucket_name(),
                    'Key': zip_key},
            ExpiresIn=3600)
        return url if url else None

    def get_bucket_name(self) -> str:
        """
        This function retrieve the bucket name from environment variables.
        :return: Bucket name.
        """
        return self.BUCKET_NAME

    def get_s3_client(self) -> boto3.client:
        """
        This function initialize the S3 client.
        :return: S3 client.
        """
        return self.s3_client

    def __get_s3_object(self, key):
        """
        This function retrieve the object from S3.
        :param key: The key of the object.
        :return: Standardized response.
        :exception ClientError: Error getting the object.
        """
        try:
            response = self.get_s3_client().get_object(Bucket=self.get_bucket_name(), Key=key)

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return http_status_code.internal_server_error(json_body={"error": "Error getting object from S3"})
            return http_status_code.ok(json_body={"message": "S3 object retrieved successfully", "data": response})
        except ClientError as error:
            return http_status_code.internal_server_error(json_body={"error": error})

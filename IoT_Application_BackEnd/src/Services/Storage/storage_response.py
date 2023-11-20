import os
import zipfile
import boto3
import http_status_code
from io import BytesIO
from Services.Storage.base_aws_service import BaseAWSService


class StorageResponse(BaseAWSService):
    BUCKET_NAME = os.environ['BUCKET_NAME']
    s3_client = None

    def __init__(self):
        BaseAWSService.__init__(self, "StorageResponse")  # base class constructor
        self.s3_client = boto3.client('s3')

    def put_object_to_s3(self, codes: dict):
        """
        This function upload an object to S3 bucket.
        :param codes: the codes generated to upload.
        """
        self.__put_object_to_s3(codes)

    def create_zip(self, keys):
        """
        This function create a zip file from a list of objects.
        :param keys: List of folders.
        """
        self.__create_zip(keys)

    # region utility methods

    def get_bucket_name(self):
        """
        This function retrieve the bucket name from environment variables.
        :return: Bucket name.
        """
        return self.BUCKET_NAME

    def get_s3_client(self):
        """
        This function initialize the S3 client.
        :return: S3 client.
        """
        return self.s3_client

    def create_url(self):
        """
        This function create a presigned url to download the zip file.
        :return: Presigned url.
        """
        return self.__create_url()

    @staticmethod
    def __handle_response(response, success_message: str) -> dict:
        """
        This function handles the API response and creates a standardized response.
        :param response: API response.
        :param success_message: Success message.
        :return: Standardized response.
        """
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        error_message = response.get('Error', {}).get('Message')

        if 200 <= status_code < 300:
            return http_status_code.ok(json_body={"message": success_message, "data": response})
        elif status_code == 403:
            return http_status_code.forbidden(json_body={"error": error_message})
        elif status_code == 404:
            return http_status_code.not_found(json_body={"error": error_message})
        elif 500 <= status_code < 500:
            return http_status_code.internal_server_error(json_body={"error": error_message})
        else:
            return http_status_code.bad_request(json_body={"error": error_message})

    def __put_object_to_s3(self, codes: dict):
        for key, value in codes.items():
            self.get_s3_client().put_object(Bucket=self.get_bucket_name(), Key=key, Body=value)

    def __get_s3_object(self, key):
        response = self.get_s3_client().get_object(Bucket=self.get_bucket_name(), Key=key)
        return self.__handle_response(response, "S3 object retrieved successfully")

    def __create_zip(self, keys):
        bucket_name = self.get_bucket_name()
        with BytesIO() as archive:
            with zipfile.ZipFile(archive, 'w') as zip_file:
                for obj in self.__list_objects(keys):
                    response = self.__get_s3_object(obj['Key'])['Body'].read()

                    if response['statusCode'] == 200:
                        file_body = response['body']['data']
                    else:
                        raise Exception(response['body']['error'])

                    zip_file.writestr(obj['Key'], file_body)

            archive.seek(0)
            self.get_s3_client().upload_fileobj(archive, bucket_name, 'code.zip')

    def __list_objects(self, keys) -> list:
        """
        This function list all the objects in a folder.
        :param keys: List of folders.
        :return: List of objects.
        """
        objects = []
        for folder_name in keys:
            try:
                response = self.get_s3_client().list_objects_v2(Bucket=self.get_bucket_name(), Prefix=folder_name)
                if 'Contents' in response:
                    objects.extend(response['Contents'])

                return objects
            except Exception as error:
                return http_status_code.internal_server_error(json_body={"error": error})

    def __create_url(self, zip_key='code.zip'):
        url = self.get_s3_client().generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.get_bucket_name(),
                    'Key': zip_key},
            ExpiresIn=3600)

        if url:
            return http_status_code.ok(json_body={"url": url})
        else:
            return http_status_code.internal_server_error(json_body={"error": "Error creating url"})

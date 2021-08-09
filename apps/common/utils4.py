import logging
import boto3
from botocore.exceptions import ClientError


def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

import requests    # To install: pip install requests

# Generate a presigned S3 POST URL
# object_name = 'chatapp/apps/common/test.txt'
# response = create_presigned_post('mybucket-chatapp', object_name)
# print(response)
# if response is None:
#     exit(1)

# Demonstrate how another Python program can use the presigned URL to upload a file
# with open(object_name, 'rb') as f:
#     files = {'file': (object_name, f)}
#     print('response',response)
#     http_response = requests.post(response['url'], data=response['fields'], files=files)
    
# If successful, returns HTTP status code 204
# logging.info(f'File upload HTTP status code: {http_response.status_code}')

# url = create_presigned_url('mybucket-chatapp', '1628248805883.webm')
# print(url)
# if url is not None:
#     response = requests.get(url)
#     print(response)

# print(response)
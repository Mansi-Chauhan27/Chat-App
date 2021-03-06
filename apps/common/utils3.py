import logging
import boto3
import json
from botocore.config import Config
from botocore.exceptions import ClientError


def create_presigned_url(bucket_name, object_name, fields=None, conditions=None, expiration=600):
    my_config = Config(
    region_name = 'us-east-2',
    signature_version = 's3v4',
    )

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',config=my_config)
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    print(response)
    # The response contains the presigned URL
    return response

result = create_presigned_url("mybucket-chatapp","toto.txt")

print(json.dumps(result, indent=4))
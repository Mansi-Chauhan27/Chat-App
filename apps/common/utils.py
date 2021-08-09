import logging
import boto3
from botocore.exceptions import ClientError
import pickle

import requests


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
        print(s3_client.list_buckets()['Buckets'])
        print(object_name,bucket_name)
        myData = {'firstName':'test','lastName':'Subramanian','title':'Manager', 'empId':'007'}
        #Serialize the object
        serializedMyData = pickle.dumps(myData)

        #Write to S3 using unique key - EmpId007
        # s3_client.put_object(Bucket=bucket_name,Key='EmpId007',Body=serializedMyData)
        url = s3_client.generate_presigned_url('put_object',Params={'Bucket':bucket_name,'Key':'test/EmpId008'},ExpiresIn=3600)
        
        print(url)
        response = requests.put(url, data=serializedMyData)
        print(response)
    except ClientError as e:
        logging.error(e)
        print(e)
        return None

    # The response contains the presigned URL
    return url


r=create_presigned_url(bucket_name='mybucket-chatapp',object_name='get_object')
# print(r)
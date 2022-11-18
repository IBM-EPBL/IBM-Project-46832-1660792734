import ibm_boto3
from ibm_botocore.client import Config, ClientError
from keys import COS_ENDPOINT, COS_API_KEY_ID, COS_INSTANCE_CRN

BUCKET_NAME = 'nutriimg'

cos = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

def upload_file(path, filename):
    cos.upload_file(Filename=path,Bucket=BUCKET_NAME,Key=filename)
    return f'https://{BUCKET_NAME}.s3.jp-tok.cloud-object-storage.appdomain.cloud/{filename}'

def delete_item(object_name):
    cos.delete_object(Bucket=BUCKET_NAME, Key=object_name)
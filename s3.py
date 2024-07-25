import boto3
import logging
import os
from dotenv import load_dotenv


load_dotenv()
AWS_SERVER_PUBLIC_KEY = os.getenv('AWS_SERVER_PUBLIC_KEY')
AWS_SERVER_SECRET_KEY = os.getenv('AWS_SERVER_SECRET_KEY')

session = boto3.Session(
    aws_access_key_id = AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key = AWS_SERVER_SECRET_KEY,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
def list_bucket():
    try:
        s3 = session.resource('s3')
        
        for bucket in s3.buckets.all():
            logging.info(bucket.name)
            print(bucket.name)
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    return True

def create_bucket(bucket_name, region=None):
    try:
        if region is None or region == 'us-east-1':  
            s3_client = session.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = session.client('s3', region_name = region)
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3_client = session.client('s3')
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    logging.info("Upload {} to {}:{} success.".format(file_name, bucket, object_name))
    return True

def download_file(save_file_path, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(save_file_path)
    try:
        s3_client = session.client('s3')
        response = s3_client.download_file(bucket, object_name, save_file_path)
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    logging.info("Download {} from {}:{} success.".format(save_file_path, bucket, object_name))
    return True

def delete_file(bucket, object_name):
    try:
        s3_client = session.client('s3')
        response = s3_client.delete_object(Bucket=bucket, Key=object_name)
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    logging.info("Delete {} from {}:{} success.".format(object_name, bucket, object_name))
    return True

def delete_bucket(bucket):
    try:
        s3_client = session.client('s3')
        response = s3_client.delete_bucket(Bucket=bucket)
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    logging.info("Delete {} success.".format(bucket))
    return True

#create_bucket("examplebucket10101010", region = "us-east-1")
#list_bucket()
#upload_file("C:\\Users\\kawam\\Pictures\\hoohoo.png", "examplebucket10101010","hoohoo.png")
#download_file("./hoohoo.png", "examplebucket10101010","hoohoo.png")
#delete_file("examplebucket10101010","collage.jpg")
#delete_bucket("examplebucket99999999")
import boto3
from botocore.exceptions import ClientError
import dotenv
import os 

"""
A Python script for working with Amazon S3
"""
ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
SECRET_KEY = 'AWS_SECRET_ACCESS_KEY'
PRI_BUCKET_NAME = 'trevisolli-bucket-001'
TRANSIENT_BUCKET_NAME = 'trevisolli-bucket-03'
F1 = 'employees_list.txt'
F2 = 'hello2.txt'
F3 = 'hello3.txt'
DIR = 'E:\\Cursos\\Pense em Python\\'
DOWN_DIR = 'C:\\temp\\downdir\\'

# Load file values 
def get_vars():
    try:
        dotenv.load_dotenv(dotenv.find_dotenv())    
        access = os.getenv(ACCESS_KEY)
        secret = os.getenv(SECRET_KEY)
        return (access,secret)
    except Exception as e:
        print("Error loading environment variables: ", e)

def create_bucket(name, s3, secure=False):
    try:
        s3.create_bucket(Bucket=name)   
        if secure:
            prevent_public_access(name, s3)
        print(f"Bucket [{TRANSIENT_BUCKET_NAME}] created.")     
    except ClientError as ce:
        print("error creating bucket:", ce)

def upload_file(bucket, directory, file, s3, s3path=None):
    file_path = directory + file 
    remote_path = s3path 
    if remote_path is None:
        remote_path = file
    try:
        s3.Bucket(bucket).upload_file(file_path, remote_path)
        print("Files were uploaded!")
    except Exception as ce:
        print("error uploading file to a bucket:", ce)        

def download_file(bucket, directory, local_name, key_name, s3):
    file_path = directory + local_name
    try:
        s3.Bucket(bucket).download_file(key_name, file_path)
    except Exception as ce:
        print("error downloading file from a bucket:", ce)        

def delete_file(bucket, keys, s3):
    objects = []
    for key in keys:
        objects.append({'Key':key})
    try:
        s3.Bucket(bucket).delete_objects(Delete={'Objects':objects})
    except Exception as ce:
        print("error deleting file from a bucket:", ce)        


def list_objects(bucket, s3):
    try:
        response = s3.meta.client.list_objects(Bucket=bucket)
        objects = []
        for content in response['Contents']:
            objects.append(content['Key'])
        return objects 
    except Exception as ce:
        print("error listing files from bucket:", ce)        

def print_objects_list(bucket, list_objects):
    print("-"*50)
    print(f"Bucket: {bucket}")
    print(f"Total Files: {len(list_objects)}")
    print("-"*50)
    print(list_objects)
    print("-"*50)

def copy_file(source_bucket, destination_bucket, source_key, destination_key, s3):
    try:
        source = {
            'Bucket' : source_bucket,
            'Key' : source_key
        }
        s3.Bucket(destination_bucket).copy(source, destination_key)
    except Exception as ce:
        print("error listing files from bucket:", ce)        


def prevent_public_access(bucket, s3):
    """Buckets and objects not public"""
    try:
        s3.meta.client.put_public_access_block(Bucket=bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls':True,
                'IgnorePublicAcls':True,
                'BlockPulicPolicy':True,
                'RestrictPublicBuckets':True
            })
    except Exception as ce:
        print("error applying policies:", ce) 

def generate_download_link(bucket, key, expiration_seconds, s3):
    try:
        s3.meta.client.generate_presigned_url('get_object', Params={
            'Bucket' : bucket,
            'Key' : key 
        }, ExpiresIn=expiration_seconds)
        print(response)
    except Exception as ce:
        print("error creating download file link:", ce) 


def delete_bucket(bucket, s3):
    try:
        s3.Bucket(bucket).delete()
    except Exception as ce:
        print("error deleting a bucket:", ce)  


def main():
    """entry point"""
    access, secret = get_vars()
    s3 = boto3.resource('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    create_bucket(PRI_BUCKET_NAME, s3, True)
    list_obj = list_objects(PRI_BUCKET_NAME, s3)
    
    if F1 not in list_obj:
        upload_file(PRI_BUCKET_NAME, DIR, F1, s3 )   
    
    generate_download_link(PRI_BUCKET_NAME, F1, 30, s3)
    print_objects_list(PRI_BUCKET_NAME, list_obj) 
    delete_bucket(PRI_BUCKET_NAME,s3)

      

if __name__ == "__main__":
    main()


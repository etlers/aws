"""
    aws configure
        - access key: 
        - secret key: 
        - region: ap-northeast-2
        - format: json
"""
import yaml
import os
import boto3

# 설정 값 불러오기
with open('rootkey.yaml', encoding='utf-8') as stream:
    awskey = yaml.safe_load(stream)

print(awskey)

def get_folder_size(bucket, prefix):
    total_size = 0
    for obj in boto3.resource('s3').Bucket(bucket).objects.filter(Prefix=prefix):
        total_size += obj.size
    return total_size

list_dt = ["2021-07-03", "2021-07-07"]
list_file = ["aaa.txt", "bbb.txt"]

bucket_name = "etlers-root"
# file_name = "aaa.txt"
prefix = "2021-07-03/"
local_dir = "/Users/etlers/Documents/sync_aws/"

# cmd = 'aws s3 ls'
# os.system(cmd)

s3 = boto3.client('s3')
idx = 0
for file_name in list_file:
    prefix = list_dt[idx] + "/"
    s3.upload_file(file_name, bucket_name, prefix + file_name)
    # Get Size as Byte.
    # 150kb = 150,000 byte or 153,600 byte
    print(prefix, get_folder_size(bucket_name, prefix))
    idx += 1
# Sync Local Folder form S3 Bucket Folder
for dt in list_dt:
    cmd = f'aws s3 sync s3://{bucket_name}/ {local_dir}'
    os.system(cmd)
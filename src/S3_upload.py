import boto3
import pandas as pd
import Config


client = boto3.client(service_name='s3', region_name=Config.s3_region_name,
                      aws_access_key_id=Config.aws_id, aws_secret_access_key=Config.aws_secret)

input_bucket_name = client.list_buckets()["Buckets"][0]["Name"]


def upload_file_to_s3(file_name, bucket_name, key):
    try:
        
        client.upload_file(file_name, bucket_name, key)

        print(f"\n\n<<<<<<<<    FILE UPLOADED TO : {bucket_name} bucket    >>>>>>>>>>>>>>>")

        return {"uploaded":True}

    except Exception as e:
        print(e)
        return {"uploaded":False}


if __name__ == "__main__":

    file_path = "C:\\Users\\adityg1\\Downloads\\AmbitionBox.xlsx"

    upload_file_to_s3(file_name=file_path,bucket_name=input_bucket_name,key="input/result.xlsx")    

    
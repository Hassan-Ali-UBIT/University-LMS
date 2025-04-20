import os
import re
import uuid
import boto3
import urllib.parse

from botocore.exceptions import ClientError
from django.conf import settings


def standard_url(file_name: str) -> str:
    return urllib.parse.quote(file_name, safe="")

def create_r2_storage_link(file_name: str) -> str:
    # return settings.R2_PUBLIC_DOMAIN + standard_url(file_name)
    return settings.R2_TEST_PUBLIC_DOMAIN + standard_url(file_name)

def sanitize_object_name(file_name: str) -> str:
    safe_name = re.sub(r'[^a-z0-9.-]', '', file_name.lower())
    safe_name = re.sub(r'[.-]{2,}', '.', safe_name)
    safe_name = safe_name.strip('.-')
    return safe_name

def generate_unique_filename(original_filename: str) -> str:
    base_name = os.path.splitext(original_filename)[0]
    ext = os.path.splitext(original_filename)[1].lower()

    safe_base = re.sub(r'[^a-z0-9-]', '', base_name.lower())[:50]
    safe_ext = re.sub(r'[^a-z0-9.]', '', ext)
    if not safe_ext.startswith('.'):
        safe_ext = f'.{safe_ext}'
    if safe_ext == '.' or len(safe_ext) > 10:
        safe_ext = '.bin'

    uuid_part = uuid.uuid4().hex
    return f"{safe_base}---{uuid_part}{safe_ext}"

def get_r2_client():
    return boto3.client(
        's3',
        endpoint_url=f'https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    )

def upload_file_to_r2(original_filename: str, file_content, directory, prefix) -> str:
    try:
        file_name = generate_unique_filename(original_filename)
        s3_client = get_r2_client()

        r2_file_name = f"{directory}/{prefix}/{file_name}"

        s3_client.upload_fileobj(
            Fileobj=file_content,
            Bucket=settings.R2_BUCKET_NAME,
            Key=r2_file_name,
            ExtraArgs={'ACL': 'public-read'}
        )

        print("Upload successful:", file_name)
        return create_r2_storage_link(r2_file_name)
    except Exception as e:
        print("Upload failed:", str(e))
        raise Exception(f"R2 upload failed: {str(e)}")

def delete_file_from_r2(file_url: str) -> bool:
    try:
        if not file_url.startswith(settings.R2_PUBLIC_DOMAIN):
            raise ValueError(f"Invalid R2 file URL: {file_url}")

        file_name = urllib.parse.unquote(file_url[len(settings.R2_PUBLIC_DOMAIN):])
        s3_client = get_r2_client()

        s3_client.delete_object(Bucket=settings.R2_BUCKET_NAME, Key=file_name)
        print("Deleted:", file_name)
        return True
    except Exception as e:
        print("Delete failed:", str(e))
        return False

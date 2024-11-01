import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from upload_service.settings import settings


def get_s3_client():
    """
    Lazily initialize and return the S3 client.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def save_file_to_s3(bucket_name: str, file_path: str, file_content: bytes) -> str:
    """
    Uploads a file to an S3 bucket and returns the file URL.

    :param bucket_name: The name of the S3 bucket.
    :param file_path: The path (including filename) where the file will be saved in S3.
    :param file_content: The binary content of the file.
    :return: The URL of the uploaded file.
    """

    try:
        s3_client = get_s3_client()
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=file_content,
            ContentType="application/octet-stream",
        )

        # Generate the URL to the file
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_path}"
        return file_url

    except NoCredentialsError:
        raise RuntimeError("S3 credentials not found.")
    except ClientError as e:
        raise RuntimeError(f"Failed to upload file to S3: {e}")

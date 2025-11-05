#Python code for image resizing:


import json
import boto3
import os
from PIL import Image
from io import BytesIO

# Initialize the S3 client outside the handler
s3 = boto3.client('s3')

# Get configuration from environment variables
DESTINATION_BUCKET = os.environ.get('DESTINATION_BUCKET')
TARGET_SIZES = [
    (150, 150),  # Thumbnail (fixed dimensions)
]

def lambda_handler(event, context):
    # 1. Extract file info from the S3 trigger event
    try:
        record = event['Records'][0]
        source_bucket = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
    except (IndexError, KeyError):
        print("Error: Invalid S3 event structure.")
        return {'statusCode': 400}

    print(f"Processing file: {file_key} from bucket: {source_bucket}")

    # 2. Download Original Image from S3
    try:
        s3_object = s3.get_object(Bucket=source_bucket, Key=file_key)
        image_content = s3_object['Body'].read()
        content_type = s3_object['ContentType']
    except Exception as e:
        print(f"Error downloading object: {e}")
        raise e

    # 3. Process and Upload Resized Images
    try:
        img = Image.open(BytesIO(image_content))
        original_format = img.format if img.format else 'JPEG'
        original_name, _ = os.path.splitext(file_key)

        for width, height in TARGET_SIZES:
            # Resize while maintaining aspect ratio (using thumbnail)
            img_copy = img.copy()
            img_copy.thumbnail((width, height))

            buffer = BytesIO()
            # Save using the original format
            img_copy.save(buffer, format=original_format)
            buffer.seek(0)

            new_key = f"resized/{original_name}_{width}x{height}.{original_format.lower()}"

            # Upload the resized image to the destination bucket
            s3.put_object(
                Bucket=DESTINATION_BUCKET,
                Key=new_key,
                Body=buffer,
                ContentType=content_type
            )
            print(f"Uploaded: {new_key}")

    except Exception as e:
        print(f"Error during image processing or upload: {e}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Image processed successfully'})
    }
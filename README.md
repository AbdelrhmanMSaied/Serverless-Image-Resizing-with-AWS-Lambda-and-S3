# Serverless-Image-Resizing-with-AWS-Lambda-and-S3
This project implements a cost-effective, event-driven solution for automatic image resizing using AWS Lambda and Amazon S3.

When an image is uploaded to a designated source S3 bucket, a Lambda function is automatically triggered. This function resizes the image and saves the resized version into a separate destination S3 bucket.

# Architecture and Components

# The solution utilizes the following AWS services:
Amazon S3 (Source Bucket): Stores the original, full-size images.
Amazon S3 (Destination Bucket): Stores the resized images.

AWS Lambda: The core compute service running the Python code (using the Pillow library) to perform the resizing.
      - Lambda Layer: Used to package the external Pillow (PIL) library dependency.
      - Lambda Trigger/Event Notification: Configured on the Source S3 Bucket to invoke the Lambda function upon a new object creation (s3:ObjectCreated:*).
      
AWS IAM: Provides the necessary permissions for the Lambda function to:
      - Read from the Source S3 Bucket.
      - Write to the Destination S3 Bucket.
      - Write logs to CloudWatch.
      
Amazon CloudWatch: Used for logging and monitoring the Lambda function's execution. 

Note:
I have used python for coding version 3.9 and i was in United States N.Virginia region, so the ARN of importing Pillow dependencies according to the region is "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pillow:1"

I will push a file that contains the python code to resize the images and stores it into the destination bucket

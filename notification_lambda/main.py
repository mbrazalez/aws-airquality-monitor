import boto3
import os 

topic = os.environ['SNS_TOPIC']
s3_bucket = os.environ['S3_BUCKET']
aws_region = os.environ['AWS_REGION']

def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']

    sns = boto3.client('sns')
    sns.publish(
        TopicArn=topic,
        Message=(
            f"Hello from lambda! Your new air quality report is ready! Check it out in the following link: "
            f"https://{s3_bucket}.s3.{aws_region}.amazonaws.com/{file_name}"
        ),
        Subject='New Air Quality Report is Ready!'
    )

    return {
        'statusCode': 200,
        'body': 'Notification sent!'
    }

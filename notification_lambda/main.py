import boto3
import os 

topic = os.environ['SNS_TOPIC']

def lambda_handler(event, context):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=topic,
        Message='New data scraped!',
        Subject='Scraping notification from Lambda'
    )

    return {
        'statusCode': 200,
        'body': 'Notification sent!'
    }

import boto3 # type: ignore
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventData')

def lambda_handler(event, context):
    response = table.scan()
    items = response.get('Items', [])
    count = len(items)

    return {
        'statusCode': 200,
        'body': json.dumps({'total_events': count})
    }

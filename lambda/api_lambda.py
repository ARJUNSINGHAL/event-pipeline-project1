import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventData')

def lambda_handler(event, context):
    try:
        # Scan all items from the table
        response = table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data retrieved successfully.',
                'data': items
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

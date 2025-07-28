import json
import boto3 # type: ignore
import datetime
import uuid

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# DynamoDB table name (must match the one created via Terraform)
TABLE_NAME = "EventData"
BUCKET_NAME = "event-pipeline-raw-data"

def lambda_handler(event, context):
    # Generate unique S3 key
    key = f"data_{datetime.datetime.now().isoformat()}.json"

    # Store the event in S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(event),
        #ACL='public-read'  # ✅ Makes the object public
    )

    # Save the event in DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        "id": str(uuid.uuid4()),  # Unique ID for DynamoDB record
        "timestamp": datetime.datetime.now().isoformat(),
        "event_data": event
    })

    # Return public S3 URL
    public_url = f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{key}"
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data stored successfully', 's3_key': key})
    }

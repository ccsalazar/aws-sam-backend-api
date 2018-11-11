from datetime import datetime
import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Comments")


def handler(event, context):

    request_body = json.loads(event["body"])
    comment = request_body["comment"]

    comment["id"] = str(uuid.uuid4())
    comment["timestamp"] = datetime.now().isoformat()
    comment["votes"] = 0

    table.put_item(Item=comment)

    return {
        'body': 'Created new comment in dynamodb table',
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

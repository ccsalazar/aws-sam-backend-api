import boto3
import json
import uuid
from datetime import datetime
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Submissions")


def handler(event, context):

    request_body = json.loads(event["body"])
    submission = request_body["submission"]
    submission["id"] = str(uuid.uuid4())
    submission["timestamp"] = datetime.now().isoformat()
    submission["votes"] = 0

    table.put_item(Item=submission)

    return {
        'body': 'Created new submission in dynamodb table',
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

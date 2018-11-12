from decimal import Decimal
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Submissions")


def default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    type(obj).__name__)


def handler(event, context):

    submission_id = event["pathParameters"]["id"]

    dynamodb_results = table.get_item(Key={"id": submission_id})

    submission = json.dumps(dynamodb_results["Item"], default=default)

    return {
        'body': submission,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

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

    request_body = json.loads(event["body"])
    request_submission_id = event["pathParameters"]["id"]

    dynamodb_results = table.get_item(Key={"id": request_submission_id})

    submission = dynamodb_results["Item"]

    if "title" in request_body:
        submission["title"] = request_body["title"]
    if "body" in request_body:
        submission["body"] = request_body["body"]

    table.put_item(Item=submission)

    submission = json.dumps(submission, default=default)

    return {
        'body': submission,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

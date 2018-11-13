from boto3.dynamodb.conditions import Attr
from decimal import Decimal
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Comments")


def default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    type(obj).__name__)


def handler(event, context):

    request_submission_id = event["pathParameters"]["id"]

    dynamodb_results = table.scan(
        FilterExpression=Attr('parentId').eq(request_submission_id)
    )

    comments = json.dumps(dynamodb_results["Items"], default=default)

    return {
        'body': comments,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

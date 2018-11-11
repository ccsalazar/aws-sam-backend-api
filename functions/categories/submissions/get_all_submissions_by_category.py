from boto3.dynamodb.conditions import Attr
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

    category = event["pathParameters"]["category"]

    dynamodb_results = table.scan(
        FilterExpression=Attr('category').eq(category)
    )

    submissions = json.dumps(dynamodb_results["Items"], default=default)

    return {
        'body': submissions,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

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

    dynamodb_results = table.scan()

    submissions = json.dumps(dynamodb_results["Items"], default=default)

    return {
        'body': submissions,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Categories")


def handler(event, context):

    dynamodb_results = table.scan(ProjectionExpression="category")

    categories = json.dumps(dynamodb_results["Items"])

    return {
        'body': categories,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

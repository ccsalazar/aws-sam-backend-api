from boto3.dynamodb.conditions import Key
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

    request_body = json.loads(event["body"])
    request_vote = request_body["vote"]
    request_comment_id = event["pathParameters"]["id"]

    dynamodb_results = table.query(
        KeyConditionExpression=Key("id").eq(request_comment_id)
    )

    comment = dynamodb_results["Items"][0]

    if request_vote == "upVote":
        comment["votes"] = int(comment["votes"]) + 1
    elif request_vote == "downVote":
        comment["votes"] = int(comment["votes"]) - 1

    table.put_item(Item=comment)

    comment = json.dumps(comment, default=default)

    return {
        'body': comment,
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }

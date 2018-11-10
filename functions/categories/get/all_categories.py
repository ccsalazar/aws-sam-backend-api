def handler(event, context):
    print("Event", event)
    print("Context", context)
    return {
        'body': 'Get All Categories Executed',
        'headers': {
            'Content-Type': 'text/plain'
        },
        'statusCode': 200
    }

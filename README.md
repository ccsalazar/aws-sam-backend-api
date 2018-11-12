
## Description

Deploying serverless applications require a cloudformation template which can be confusing to configure. In this repo I try to outline a simple workflow for working and deploying a sample backend api utilizing the Python 3.6 runtime, Api Gateway, Lambda, CloudFormation, SAM, and the AWS CLI.

## Getting Started

` git clone git@github.com:ccsalazar/aws-sam-backend-api.git `



## CloudFormation w/ SAM Template Anatomy

To read more about the CloudFormation Template Anatomy read the docs [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html) and the SAM properties [here](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md). SAM properties are allowed in CloudFormation Templates with the use of the **Transform: 'AWS::Serverless-2016-10-31'** property.

## The REST API we will be creating


The following endpoints are available:

| Endpoints       | Usage          | Params         |
|-----------------|----------------|----------------|
| `GET /categories` | Get all of the categories available for the app. List is found in `categories.js`. Feel free to extend this list as you desire. |  |
| `GET /:category/posts` | Get all of the posts for a particular category. |  |
| `GET /posts` | Get all of the posts. Useful for the main page when no category is selected. |  |
| `POST /posts` | Add a new post. | **id** - UUID should be fine, but any unique id will work <br> **timestamp** - [Timestamp] Can in whatever format you like, you can use `Date.now()` if you like. <br> **title** - [String] <br> **body** - [String] <br> **author** - [String] <br> **category** -  Any of the categories listed in `categories.js`. Feel free to extend this list as you desire. |
| `GET /posts/:id` | Get the details of a single post. | |
| `POST /posts/:id` | Used for voting on a post. | **option** - [String]: Either `"upVote"` or `"downVote"`. |
| `PUT /posts/:id` | Edit the details of an existing post. | **title** - [String] <br> **body** - [String] |
| `DELETE /posts/:id` | Sets the deleted flag for a post to 'true'. <br> Sets the parentDeleted flag for all child comments to 'true'. | |
| `GET /posts/:id/comments` | Get all the comments for a single post. | |
| `POST /comments` | Add a comment to a post. | **id** - Any unique ID. As with posts, UUID is probably the best here. <br> **timestamp** - [Timestamp] Get this however you want. <br> **body** - [String] <br> **author** - [String] <br> **parentId** - Should match a post id in the database. |
| `GET /comments/:id` | Get the details for a single comment. | |
| `POST /comments/:id` | Used for voting on a comment. | **option** - [String]: Either `"upVote"` or `"downVote"`.  |
| `PUT /comments/:id` | Edit the details of an existing comment. | **timestamp** - timestamp. Get this however you want. <br> **body** - [String] |
| `DELETE /comments/:id` | Sets a comment's deleted flag to `true`. | &nbsp; |


## How It Works

Your Lambda functions are compressed to a zipped folder and copied to an s3 bucket. The sam template contains the definitions of your Lambda functions which has 3 key properties CodeUri, Handler, and Events. The CodeUri is your s3 bucket/key where you copied your Lambda functions. The Handler is the path to your function. The Events is where you define what triggers your Lambda function. There are a list of Events but for this use case the one we are most interested in is the Api trigger. Here we define the resource, method, etc. that will trigger our Lambda to execute.


## Deployment

### Before you can deploy

* Install AWS CLI and set up your aws credentials.

* Create an S3 bucket to store your Lambda Functions that your template will be referencing
    ```
    aws s3 mb s3://<bucket-name>
    ```
* Copy your functions to S3
    ```
    zip -r functions.zip functions

    aws s3 cp functions.zip s3://<bucket-name>/functions.zip
    ```

### Deploying

* Package your sam.yaml template for cloudformation
    
    ```
    aws cloudformation package \
    --template-file sam.yaml \
    --s3-bucket <bucket-name> \
    --output-template-file sam-packaged.yaml
    ```

* Deploy to a cloudformation stack. If the stack doesn't exist then it will be created, otherwise the existing stack will be updated

    ```
    aws cloudformation deploy \
    --template-file ./sam-packaged.yaml \
    --stack-name <stack-name> \
    --capabilities CAPABILITY_IAM
    ```

## Sidenotes or issues to improve on

* Marshalling DyanamoDb data without types e.g. { "data": {"S" : "test data" } } instead you want { "data": "test data" }. Explain the difference between boto3 Client and Table
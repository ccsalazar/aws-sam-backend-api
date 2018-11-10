
## Deployment

### Before you deploy

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

* Deploy to cloudformation to a stack. If the stack doesn't exist then it will be created, otherwise the existing stack will be updated

    ```
    aws cloudformation deploy \
    --template-file ./sam-packaged.yaml \
    --stack-name <stack-name> \
    --capabilities CAPABILITY_IAM
    ```
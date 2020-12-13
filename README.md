# Government Identity Verification Engine

## Transaction Logging Service

## Pre-requisites
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Chalice Template](https://github.com/folksgl/chalice-cicd-app)

## Building with the CI/CD Pipeline
Building with the CI/CD pipeline can be done as follows:
```sh
cd pipeline/
cdk deploy --ConnectionSecretId=<my-connection-id>
```
where `ConnectionSecretId` is the CodeStar connection ARN for the repository defined in `pipeline/app.py`.

## Build/Local Deploy

First set up a local environment, see the Chalice Template in the Pre-reqs.

Then switch to the app with `cd app`.

Finally, launch the local server with `chalice local`.

### Database
For local testing only...

`aws cloudformation deploy --template-file dynamodb_cf_template.yaml --stack-name transaction-logs-db`

Launches the DB, must redeployed if any DB changes are made.


### Available Endpoints

`/`

`/item`


## Example POST Request
```
http://127.0.0.1:8000/item

{
    "id" : "this is the ID",
    "text" : "text for item"
}

```

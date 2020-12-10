# Government Identity Verification Engine

## Transaction Logging Service

## Pre-requisites
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Chalice Template](https://github.com/folksgl/chalice-cicd-app)

### Build/Local Deploy

First set up a local environment, see the Chalice Template in the Pre-reqs.

Then switch to the app with `cd app`.

Finally, launch the local server with `chalice local`.

### Database

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
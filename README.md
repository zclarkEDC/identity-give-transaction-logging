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
where `ConnectionSecretId` is the SecretsManager secret containing the CodeStar connection ARN for the repository defined in `pipeline/app.py`. Note -- the JsonKey for the secret must be 'arn'.

## Build/Local Deploy

First set up a local environment, see the Chalice Template in the Pre-reqs.

Then switch to the app with `cd app`.

Finally, launch the local server with `chalice local`.

*Note: any endpoints with database operations will not function locally.


### Available Endpoints

`/`

`/item`


## Example POST Request

Use the deployed aws endpoint for making requests to endpoints that utilize the database.

```

{
    "id" : "this is the ID",
    "text" : "text for item"
}

```

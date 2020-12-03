# Government Identity Verification Engine

## Transaction Logging Service

## Pre-requisites
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Docker](https://www.docker.com/products/docker-desktop)

### Build/Local Deploy

`npm install`

Installs npm dependencies

`sam build`

Builds the project.

`sam local start-api`

Starts the REST API on `http://127.0.0.1:3000`


### Available Endpoints
POST, PUT
`/transaction`

GET, DELETE
`/transaction/{UUID}/{Timestamp}`


## Example POST Request
```
http://127.0.0.1:3000/transaction?TableName=TransactionLogs

{
    "TableName": "TransactionLogs",
    "ServiceType": "Proofing Services",
    "CSP": "Idemia",
    "Result": "in-progress",
    "ProofingStatus": "attending in person proofing"
}

```
TableName is the only required attribute, currently considering separating customers into different tables.

UUID is derived from the `context.awsRequestId;`, but for testing the PUT Request endpoint you can comment out the UUID and Timestamp.
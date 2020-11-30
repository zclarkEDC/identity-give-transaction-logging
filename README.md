# Government Identity Verification Engine

## Transaction Logging Service

## Pre-requisites
- [Maven](https://maven.apache.org/) 
- [OpenJDK 8](https://developers.redhat.com/products/openjdk/download)
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

`/transaction`

## Example POST Request
```
http://127.0.0.1:3000/transaction?TableName=TransactionLogs

{
    "TableName": "TransactionLogs",
        "Item": {
            "UUID": "110",
            "Timestamp": 1605873564,
            "Customer": "test man",
            "ServiceType": "Proofing Services",
            "CSP": "Idemia",
            "Result": "in-progress",
            "ProofingStatus": "attending in person proofing"

        }
    
}

```
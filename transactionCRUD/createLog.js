'use strict';
console.log('Loading function');
const doc = require('dynamodb-doc');
const dynamo = new doc.DynamoDB();
const TableName = process.env.TABLE_NAME;
exports.handler = async (event, context) => {

    let body;
    let statusCode = '201';
    const headers = {
        'Content-Type': 'application/json',
    };

    //add UUID and Timestamp to the request body
    const reqBody = JSON.parse(event.body);
    reqBody["UUID"] = context.awsRequestId; //comment this out if you want to specify your own UUID
    reqBody["Timestamp"] = Date.now();     //comment this out if you want to make a request with your own Timestamp
    
    //send to the DynamoDB table
    try {
        body = await dynamo.putItem({
            TableName,
            Item: reqBody
        }, function (err, data) {
            if (err) console.log('Error:', err.message, err.stack); // an error occurred
            else console.log('Success:',data);                     // successful response
        }).promise();
    }
    catch (err) {
        body = err;
        statusCode = body.statusCode;
    }
    finally {
        body = JSON.stringify(body);
    }
    return { body, statusCode, headers };
}
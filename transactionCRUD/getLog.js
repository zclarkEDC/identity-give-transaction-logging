'use strict';
console.log('Loading function');
var doc = require('aws-sdk');
const dynamo = new doc.DynamoDB();
const TableName = process.env.TABLE_NAME;
exports.handler = async (event, context) => {

    let body;
    let statusCode = '200';
    const headers = {
        'Content-Type': 'application/json',
    };
    //send to the DynamoDB table
    try {
        var params = {
            TableName,
            Key: {
              'UUID': {S: event.pathParameters.UUID},
              'Timestamp': {N: event.pathParameters.Timestamp}
            }
          };
        body = await dynamo.getItem(params, function (err, data) {
            if (err) console.log('Error:', err.message, err.stack); // an error occurred
            else console.log('Success:', data.Item);                     // successful response
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

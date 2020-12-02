/* this is working code
const { DynamoDB } = require('aws-sdk');
const db = new DynamoDB.DocumentClient();


module.exports.create = async event => {
    console.log('Received event:', JSON.stringify(event, null, 2));
    const reqBody = JSON.parse(event.body);
    console.log('REEEE', JSON.stringify(reqBody));
    const transactionLog = {
        UUID: reqBody.UUID,
        Timestamp: reqBody.Timestamp,
        tester: reqBody.Customer
    };
    console.log('REEEE', JSON.stringify(transactionLog));
    await db.put({
        TableName: event.queryStringParameters.TableName,
        Item: transactionLog
    }).promise();

    
    return {statusCode: 200, body: JSON.stringify(transactionLog)};

}

*/
/* iteration 2, working 
const { DynamoDB } = require('aws-sdk');
const db = new DynamoDB.DocumentClient();




exports.handler = async (event, context, callback) => {

    let response;
    let statusCode = 201;
    try {
        console.log('Received event:', JSON.stringify(event, null, 2));
        const reqBody = JSON.parse(event.body);
        console.log('REEEE', JSON.stringify(reqBody));
        const transactionLog = {
            UUID: reqBody.UUID,
            Timestamp: reqBody.Timestamp,
            tester: reqBody.Customer
        };
        console.log('REEEE', JSON.stringify(transactionLog));
        await db.put({
            TableName: event.queryStringParameters.TableName,
            Item: transactionLog
        }).promise();
        response = JSON.stringify(transactionLog);
    }
    catch (err) {
        response = err.message;
        statusCode = '400';

    }
    return {
        statusCode,
        body: response
    };



    //return {statusCode: 200, body: JSON.stringify(transactionLog)};

}
*/
'use strict';

console.log('Loading function');

const doc = require('dynamodb-doc');

const dynamo = new doc.DynamoDB();

//const { uuid } = require('uuidv4');
const { v4: uuidv4 } = require('uuid');
exports.handler = async (event, context, callback) => {

    let response;
    let statusCode = 201;
    
    try {
        //console.log('Received event:', JSON.stringify(event, null, 2));
        const reqBody = JSON.parse(event.body);
        console.log('REEEE', JSON.stringify(reqBody));
        var d = Date.now();
        const transactionLog = {
            UUID: uuidv4(),
            Timestamp: d,
            tester: reqBody.Customer
        };
        console.log('REEEE', JSON.stringify(transactionLog));
        response = await dynamo.putItem({
            TableName: event.queryStringParameters.TableName,
            Item: transactionLog
        }, function (err, data) {
            if (err) console.log('it fucked up', err.message, err.stack); // an error occurred
            else console.log('it worked?',data);           // successful response
        }).promise();
    }
    catch (err) {
        response = err.message;
        statusCode = 400;

    }
    finally {
        response = JSON.stringify(response);
    }
    return {
        statusCode,
        body: response
    };




}
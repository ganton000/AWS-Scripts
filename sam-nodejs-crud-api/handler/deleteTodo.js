const AWS = require("aws-sdk");

const TODO_TABLE = process.env.TODO_TABLE;
const ddb = new AWS.DynamoDB.DocumentClient();

let body;
let statusCode = 200;
const headers = {
    "Content-Type": "application/json",
};

exports.deleteTodo = async (event, context) => {
    const params = {
        TableName: TODO_TABLE,
        Key: {
            id: event.pathParameters.id,
        },
    };

    await ddb.delete(params).promise();
    body = `Delete todo ${event.pathParameters.id}`;

    return {
        statusCode,
        body,
        headers,
    };
};

const AWS = require("aws-sdk");

const TODO_TABLE = process.env.TODO_TABLE;
const ddb = new AWS.DynamoDB.DocumentClient();

let body;
let statusCode = 200;
const headers = {
    "Content-Type": "application/json",
};

exports.updateTodo = async (event, context) => {
    const datetime = new Date().toISOString();
    const data = JSON.parse(event.body);

    let body;
    let statusCode = 200;
    const headers = {
        "Content-Type": "application/json",
    };

    console.log("Data::", data);

    if (typeof data.todo !== "string" || typeof data.checked !== "boolean") {
        console.error("Value of todo or done is invalid");
        return;
    }

    const params = {
        TableName: TODO_TABLE,
        Key: {
            id: event.pathParameters.id,
        },
        ExpressionAttributeNames: {
            "#todo_text": "todo",
        },
        ExpressionAttributeValues: {
            ":todo": data.todo,
            ":checked": data.checked,
            ":updatedAd": datetime,
        },
        UpdateExpression:
            "SET #todo_text = :todo, checked = :checked, updatedAt = :updatedAt",
        ReturnValues: "ALL_NEW",
    };

    try {
        body = await ddb.update(params).promise();
    } catch (err) {
        statusCode = 400;
        body = err.message;
        console.log(err);
    } finally {
        body = JSON.stringify(body.Attributes);
    }

    return {
        statusCode,
        body,
        headers,
    };
};

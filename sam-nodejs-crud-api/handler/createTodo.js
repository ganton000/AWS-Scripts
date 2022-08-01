const AWS = require("aws-sdk");
const uuid = require("uuid");

const TODO_TABLE = process.env.TODO_TABLE;
const ddb = new AWS.DynamoDB.DocumentClient();

//npm install should be inside handler folder as this is where package.json is

exports.createTodo = async (event, context) => {
    const timestamp = new Date().getTime();
    const data = JSON.parse(event.body);
    let body;
    let statusCode = 200;
    const headers = {
        "Content-Type": "application/json",
    };

    const params = {
        TableName: TODO_TABLE,
        Item: {
            id: uuid.v1(),
            todo: data.todo,
            checked: false,
            createdAt: timestamp,
            updatedAt: timestamp,
        },
    };

	if (typeof data.todo !== "string") {
		console.error("Validation Failed");
		return;
	}

	try {
		body = await ddb.put((params)).promise();
	} catch (err) {
		statusCode = 400;
		body = err.message;
		console.log(err)
	} finally {
		body = JSON.stringify(body)
	}

	return {
		statusCode,
		body,
		headers
	}
};

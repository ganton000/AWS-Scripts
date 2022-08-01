"use strict";
const AWS = require("aws-sdk");
const ses = new AWS.SES();

module.exports.createContact = async (event, context) => {
    console.log("Received:::", event);
    const { to, from, subject, message } = JSON.parse(event.body);

    if (!to || !from || !subject || !message) {
        return {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": false, //required for cookies
                "Content-Type": "application/json",
            },
            statusCode: 400,
            body: JSON.stringify({
                message: " to or from ... are not set properly!",
            }),
        };
    }

    const params = {
        Destination: {
            ToAddresses: [to],
        },
        Message: {
            Body: {
                Text: { Data: message },
            },
            Subject: { Data: subject },
        },
        Source: from,
    };

    try {
        await ses.sendEmail(params).promise();
        return {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": false, //required for cookies
                "Content-Type": "application/json",
            },
            statusCode: 200,
            body: JSON.stringify({
                message: "email sent successfully!",
                success: true,
            }),
        };
    } catch (err) {
        console.error(err);

        return {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": false, //required for cookies
                "Content-Type": "application/json",
            },
            statusCode: 400,
            body: JSON.stringify({
                message: "The email has failed to send",
                success: true,
            }),
        };
    }
};

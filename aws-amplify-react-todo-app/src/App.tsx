import React, { useEffect, useState } from "react";
import { Amplify, API, graphqlOperation } from "aws-amplify";
import { createTodo } from "./graphql/mutations";
import { listTodos } from "./graphql/queries";
import awsExports from "./aws-exports";

import "./App.css";

//configures Amplify with AWS credentials
Amplify.configure(awsExports);

function App() {
    return <div>App</div>;
}

export default App;

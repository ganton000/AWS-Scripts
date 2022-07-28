import React, { useEffect, useState } from "react";
import { Amplify, API, graphqlOperation } from "aws-amplify";
import { createTodo } from "./graphql/mutations";
import { listTodos } from "./graphql/queries";
import awsExports from "./aws-exports";

import "./App.css";

//configures Amplify with AWS credentials
Amplify.configure(awsExports);

const initialState = {
    name: "",
    description: "",
};

type Todos = {
  [key: string]: string
}

function App() {
    const [formState, setFormState] = useState(initialState);
    const [todos, setTodos] = useState([] as Todos[]);

    const setInput = (key: any, val: any): any => {
        setFormState({ ...formState, [key]: val });
    };

    const fetchTodos = async (): Promise<any> => {
        try {
            const todoData: any = await API.graphql(
                graphqlOperation(listTodos)
            );

            const todos: any = todoData.data.listTodos.items;
            setTodos(todos);
        } catch (err) {
            console.log("error fetching todos");
        }
    };

    const addTodo = async (): Promise<any> => {
        try {
            if (!formState.name || !formState.description) return;

            const todo = { ...formState };
            setTodos([...todos, todo]);
            setFormState(initialState);

            await API.graphql(
                graphqlOperation(createTodo, {
                    input: todo,
                })
            );
        } catch (error) {
            console.log("error creating todo: ", error);
        }
    };

    useEffect(() => {
        fetchTodos();
    }, []);

    return (
        <div className="container">
            <h2>Amplify Todos</h2>
            <input
                onChange={(event) => setInput("name", event.target.value)}
                value={formState.name}
                placeholder="Name"
            />
            <input
                onChange={(event) =>
                    setInput("description", event.target.value)
                }
                value={formState.description}
                placeholder="Description"
            />
            <button onClick={addTodo}>Create Todo</button>
            {todos.map((todo, index) => (
                <div key={todo.id ? todo.id : index} className="todo">
                    <p className="todoName">{todo.name}</p>
                    <p className="todoDescription">{todo.description}</p>
                </div>
            ))}
        </div>
    );
}

export default App;

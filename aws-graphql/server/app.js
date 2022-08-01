const express = require("express");
const { graphqlHTTP } = require("express-graphql");

const app = express();

app.use('/graphql', graphqlHTTP({
	graphiql: true
}))

const PORT = 4000;

app.listen(PORT, () => {
    console.log(`Listening in on PORT: ${PORT}`);
});

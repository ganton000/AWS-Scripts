const {
    GraphQLObjectType,
    GraphQLID,
    GraphQLString,
    GraphQLInt,
    GraphQLSchema,
} = require("graphql");

//Types
const UserType = new GraphQLObjectType({
    name: "User",
    description: "Documentation for User...",
    fields: () => ({
        id: {
            type: GraphQLString,
        },
        name: {
            type: GraphQLString,
        },
        age: {
            type: GraphQLInt,
        },
    }),
});

//Root Query
const RootQuery = new GraphQLObjectType({
    name: "RootQueryType",
    description: "Description",
    fields: {
        user: {
            type: UserType,
            args: { id: { type: GraphQLString } },

            resolve(parent, args) {
                //get and return data from data source
            },
        },
    },
});

module.exports = new GraphQLSchema({
    query: RootQuery,
});

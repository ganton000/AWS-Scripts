const {
    GraphQLObjectType,
    GraphQLID,
    GraphQLString,
    GraphQLInt,
    GraphQLSchema,
} = require("graphql");

let _ = require("lodash");

let usersData = [
    {
        id: "345",
        name: "Anton",
        age: 32,
        profession: "Engineer",
    },
    {
        id: "123",
        name: "Lobert",
        age: 43,
        profession: "Teacher",
    },
];

let hobbiesData = [
    {
        id: "1",
        title: "Programming",
        description: "Using computers",
    },
    {
        id: "2",
        title: "Fencing",
        description: "Using swords",
    },
];

let postData = [
    {
        id: "1",
        comment: "first comment",
    },
    {
        id: "2",
        comment: "second comment",
    },
];

//Types
const UserType = new GraphQLObjectType({
    name: "User",
    description: "Documentation for User...",
    fields: () => ({
        id: {
            type: GraphQLID,
        },
        name: {
            type: GraphQLString,
        },
        age: {
            type: GraphQLInt,
        },
        profession: {
            type: GraphQLString,
        },
    }),
});

const HobbyType = new GraphQLObjectType({
    name: "Hobby",
    description: "Hobby description",
    fields: () => ({
        id: {
            type: GraphQLID,
        },
        title: {
            type: GraphQLString,
        },
        description: {
            type: GraphQLString,
        },
    }),
});

const PostType = new GraphQLObjectType({
    name: "Post",
    description: "Post description",
    fields: () => ({
        id: {
            type: GraphQLID,
        },
        comment: {
            type: GraphQLString,
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
            args: { id: { type: GraphQLID } },

            resolve(parent, args) {
                //get and return data from data source

                return _.find(usersData, { id: args.id });
            },
        },
        hobby: {
            type: HobbyType,
            args: { id: { type: GraphQLID } },

            resolve(parent, args) {
                return _.find(hobbiesData, { id: args.id });
            },
        },
        post: {
            type: PostType,
            args: { id: { type: GraphQLID } },
            resolve(parent, args) {
                return _.find(postData, { id: args.id });
            },
        },
    },
});

module.exports = new GraphQLSchema({
    query: RootQuery,
});

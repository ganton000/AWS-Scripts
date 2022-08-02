const {
    GraphQLObjectType,
    GraphQLID,
    GraphQLString,
    GraphQLInt,
    GraphQLSchema,
    GraphQLList,
} = require("graphql");

let _ = require("lodash");

let usersData = [
    {
        id: "1",
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
        userId: "1",
    },
    {
        id: "3",
        title: "Chess",
        description: "Playing chess games",
        userId: "1",
    },
    {
        id: "2",
        title: "Fencing",
        description: "Using swords",
        userId: "2",
    },
];

let postData = [
    {
        id: "1",
        comment: "first comment",
        userId: "1",
    },
    {
        id: "3",
        comment: "another comment",
        userId: "1",
    },
    {
        id: "2",
        comment: "second comment",
        userId: "2",
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

        posts: {
            type: new GraphQLList(PostType),
            resolve(parent, args) {
                return _.filter(postData, { userId: parent.id });
            },
        },

        hobbies: {
            type: new GraphQLList(HobbyType),
            resolve(parent, args) {
                return _.filter(hobbiesData, { userId: parent.id });
            },
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
        user: {
            type: UserType,
            resolve(parent, args) {
                return _.find(usersData, { id: parent.userId });
            },
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
        user: {
            type: UserType,
            resolve(parent, args) {
                return _.find(usersData, { id: parent.userId });
            },
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
        users: {
            type: new GraphQLList(UserType),
            resolve(parent, args) {
                return usersData;
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

//Mutations
const Mutation = new GraphQLObjectType({
    name: "Mutation",
    fields: {
        createUser: {
            type: UserType,
            args: {
                id: { type: GraphQLID },
                name: { type: GraphQLString },
                age: { type: GraphQLInt },
                profession: { type: GraphQLString },
            },
            resolve(parent, args) {
                let user = {
                    name: args.name,
                    age: args.age,
                    profession: args.profession,
                };
                return user;
            },
        },
        createPost: {
            type: PostType,
            args: {
                id: { type: GraphQLID },
                comment: { type: GraphQLString },
                userId: { type: GraphQLID },
            },
            resolve(parent, args) {
                let post = {
                    comment: args.comment,
                    userId: args.userId,
                };
                return post;
            },
        },
        createHobby: {
            type: HobbyType,
            args: {
                id: { type: GraphQLID },
                title: { type: GraphQLString },
                description: { type: GraphQLString },
                userId: { type: GraphQLID },
            },
            resolve(parent, args) {
                let hobby = {
                    title: args.title,
                    description: args.description,
                    userId: args.userId,
                };
                return hobby;
            },
        },
    },
});

module.exports = new GraphQLSchema({
    query: RootQuery,
    mutation: Mutation,
});

const Twitter = require("twitter")
const neo4j = require("neo4j-driver")

const client = new Twitter({
    consumer_key: 'bKJovi2dPl7oQLHu6pURE2XLd',
    consumer_secret: 'BZnu88YplB6QGgC8ylNfLtywLi6ENtVgQQ9sxpQ2lNhslPW1AE',
    // bearer_token: "AAAAAAAAAAAAAAAAAAAAAEFQFwEAAAAA6owdsX%2F6OJajChyCZYF4KaFvC3o%3Du8um6NvVN1NbBudZyidmTse0b0CnSxOqmCATRwPraJqryK9Sx8",
    access_token_key: "519797761-JTNA2uumMwRTsigDheSmMmz6PYnXHl6B63XchPha",
    access_token_secret: "7OErt1pR2DzvlFIO23LyK9e4K0EgLSjuVr8Mpr088ewBF"
})

// Sergioherranz90, juanjops_valmy

const users = ["juanjops_valmy"]

const driver = neo4j.driver('bolt://localhost:7687', neo4j.auth.basic("neo4j", "twitter"))

const main = async (users) => {

    await Promise.all(users.map(user => load_user(user)))
    await Promise.all(users.map(user => load_one_user_data(user)))
    await driver.close()

}

async function load_user(user) {
    
    try {
        const response = await client.get('users/lookup', {screen_name: user})
        const session = driver.session()
        await session.run(
            'MERGE (person:Person {name: $name, screen_name: $screen_name, location: $location, description: $description}) RETURN person',
            {name: response[0].name, screen_name: response[0].screen_name, location: response[0].location, description: response[0].description}
        )
        await session.close()
    } catch {
        console.log(error)
    }

}

async function load_one_user_data(user) {

    const friends = await get_friends(user)
    await Promise.all(friends.map(friend => load_user(friend)))
    await Promise.all(friends.map(friend => load_follow_relationship(user, friend)))
    await Promise.all(friends.map(friend => load_user_tweets(friend)))

}

async function get_friends(user) {

    let friends = []
    let cursor = -1
    try {
        while (cursor != 0) {
            const response = await client.get('friends/list', {screen_name: user, cursor: cursor})
            response.users.forEach(user => friends.push(user.screen_name))
            cursor = response.next_cursor
        }
        return friends
    } catch {
        console.log(user + " no friends retrieved")
    }

}

async function load_follow_relationship(user, friend) {
    
    try {
        const session = driver.session()
        await session.run(
            'MATCH (a:Person{screen_name: $user_name}), (b:Person{screen_name: $friend_name}) MERGE (a)-[:FOLLOWS]->(b) RETURN a, b',
            {user_name: user, friend_name: friend}
        )
        await session.close()
    } catch {
        console.log(error)
    }

}

async function load_user_tweets(user) {
    
    try {
        const tweets = await client.get('statuses/user_timeline', {screen_name: user, count: 10})
        await Promise.all(tweets.map(tweet => load_tweet(user, tweet)))
    } catch {
        console.log(error)
    }

}

async function load_tweet(user, tweet) {
    
    try {
        const session = driver.session()
        await session.run(
            'MERGE (b:Tweet{text: $tweet_text}) WITH b MATCH (a:Person{screen_name: $user_name}) MERGE (a)-[:POSTS]->(b) RETURN a, b',
            {user_name: user, tweet_text: tweet.text}
        )
        await session.close()
    } catch {
        console.log(error)
    }

}

main(users)


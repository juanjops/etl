const Twitter = require("twitter")
const axios = require("axios")
const C = require("../constants.js")

const client = new Twitter({
    consumer_key: 'bKJovi2dPl7oQLHu6pURE2XLd',
    consumer_secret: 'BZnu88YplB6QGgC8ylNfLtywLi6ENtVgQQ9sxpQ2lNhslPW1AE',
    bearer_token: "AAAAAAAAAAAAAAAAAAAAAEFQFwEAAAAA6owdsX%2F6OJajChyCZYF4KaFvC3o%3Du8um6NvVN1NbBudZyidmTse0b0CnSxOqmCATRwPraJqryK9Sx8"
    // access_token_key: "519797761-JTNA2uumMwRTsigDheSmMmz6PYnXHl6B63XchPha",
    // access_token_secret: "7OErt1pR2DzvlFIO23LyK9e4K0EgLSjuVr8Mpr088ewBF"
})

// Sergioherranz90, juanjops_valmy

const post_url = `http://127.0.0.1:${C.SERVER_PORT}/tweets`

const user = "juanjops_valmy"

const main = async (user) => {

    const friends = await get_friends(user)
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

async function load_user_tweets(user) {
    
    try {
        const tweets = await client.get('statuses/user_timeline', {screen_name: user, count: 200})
        await Promise.all(tweets.map(tweet => load_tweet(user, tweet)))
    } catch {
        console.log(error)
    }

}

async function load_tweet(user, tweet) {
    
    try {

        await axios.post(post_url, {
            id_str: tweet.id_str, 
            text: tweet.text, 
            screen_name: user, 
            created_at: tweet.created_at
        })

    } catch {
        console.log("post fail to server")
    }

}

main(user)


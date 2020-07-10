const C = require("./constants.js")
const express = require("express")
const path = require("path")
require("./db/mongoose")
const dataScience = require("./routers/datasciences.js")
const marketingRouter = require("./routers/marketings.js")
const clickRouter = require("./routers/click.js")
const twitter = require("./routers/tweets.js")

const app = express()
const port = process.env.PORT || C.SERVER_PORT

app.use(express.json())

app.use(dataScience)

app.use(marketingRouter)

app.use(clickRouter)

app.use(twitter)

app.use(express.static(path.join(__dirname, "./public")))

app.listen(port, () => {
    console.log("Server is up on port " + port)
})

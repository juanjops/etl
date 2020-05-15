const C = require("./constants.js")
const express = require("express")
const path = require("path")
require("./db/mongoose")
const dataScience = require("./routers/data-science.js")
const marketingRouter = require("./routers/marketing.js")
const clickRouter = require("./routers/click.js")

const app = express()
const port = process.env.PORT || C.SERVER_PORT

app.use(express.json())

app.use(dataScience)

app.use(marketingRouter)

app.use(clickRouter)

app.use(express.static(path.join(__dirname, "./public")))

app.listen(port, () => {
    console.log("Server is up on port " + port)
})

const C = require("./constants.js")
const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/data-science.js")
const marketingRouter = require("./routers/marketing.js")

const app = express()
const port = process.env.PORT || C.SERVER_PORT

app.use(express.json())

app.use(linkedinRouter)

app.use(marketingRouter)

app.listen(port, () => {
    console.log("Server is up on port " + port)
})

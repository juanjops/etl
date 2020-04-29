const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin")


const app = express()
const port = process.env.PORT || 3000

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port "  + port)
})
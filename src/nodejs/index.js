const C = require("./constants.js")
const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin.")
const linkedin_scraper = require("./scraping/linkedin.js")

const app = express()
const port = process.env.PORT || C.SERVER_PORT

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port " + port)
})

const JOB_SEARCH_SPECS = {
    "key_words": "data science",
    "location" : "Dublin",
    "time_range": "Past Week"
}

linkedin_scraper(JOB_SEARCH_SPECS)

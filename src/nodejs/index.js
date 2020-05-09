const C = require("./constants.js")
const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin.js")
const linkedin_scraper = require("./scraping/linkedin.js")
const marianna_scraper = require("./scraping/marianna.js")

const app = express()
const port = process.env.PORT || C.SERVER_PORT

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port " + port)
})

const JOB_SEARCH_SPECS = {
    "key_words": "data science",
    "location" : "London",
    "time_range": "Past 24 hours"
}

linkedin_scraper(JOB_SEARCH_SPECS)

const MARIANNA_JOB_SEARCH_SPECS = {
    "key_words": "marketing",
    "location" : "Madrid",
    "time_range": "Past 24 hours"
}

// marianna_scraper(MARIANNA_JOB_SEARCH_SPECS)

const C = require("./constants.js")
const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin.js")
const linkedin_scraper = require("./scraping/linkedin.js")
const insert_csv = require("./csv_to_mongo/csv_to_mongo.js")

const app = express()
const port = process.env.PORT || C.SERVER_PORT

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port " + port)
})

const JOB_SEARCH_SPECS = {
    "key_words": "data science",
    "location" : "Madrid",
    "time_range": "Past 24 hours"
}

linkedin_scraper(JOB_SEARCH_SPECS)

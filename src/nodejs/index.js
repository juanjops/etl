const C = require("./constants.js")
const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin")
const getJobsId = require("./scraping/linkedin/jobs_id")
const getJobContent = require("./scraping/linkedin/job_content")

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

const main = async (jobs_search_specs) => {
    try {
        const jobs_id = await getJobsId(jobs_search_specs)
        jobs_id.map(job_id => getJobContent(job_id))
    } catch (e) {
        console.log(e)
    }
}

main(JOB_SEARCH_SPECS)

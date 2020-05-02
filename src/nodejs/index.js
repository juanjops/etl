const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin")
const getJobsId = require("./scraping/linkedin/jobs_id")
const getJobContent = require("./scraping/linkedin/job_content")


const app = express()
const port = process.env.PORT || 3000

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port "  + port)
})

const main = async () => {

    try {
        const jobs_id = await getJobsId()
        jobs_id.map(job_id => getJobContent(job_id))
    } catch (e) {
        console.log(e)
    }
    
}

main()

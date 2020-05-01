const express = require("express")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin")
const getJobsContent = require("./scraping/scraping")


const app = express()
const port = process.env.PORT || 3000

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port "  + port)
})

jobs_id = ["1806342384", "1793103579"]

jobs_id.map(job_id => getJobsContent(job_id))

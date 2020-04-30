const express = require("express")
const axios = require("axios")
const cheerio = require("cheerio")
require("./db/mongoose")
const linkedinRouter = require("./routers/linkedin")


const app = express()
const port = process.env.PORT || 3000

app.use(express.json())

app.use(linkedinRouter)

app.listen(port, () => {
    console.log("Server is up on port "  + port)
})



const urls = ["https://www.linkedin.com/jobs/view/1806342384", "https://www.linkedin.com/jobs/view/1793103579"]

const post_url = "http://127.0.0.1:3000/linkedin"

const getWebsiteContent = async (url) => {

    try {
        const res_url = await axios.get(url)
        const $ = cheerio.load(res_url.data)
        let parsedResults = {}
        $('.topcard__content .topcard__content-left').map((i, el) => {
            const jobid = $(el).find('h1').text()
            const title = $(el).find('h3').text()
            parsedResults = {jobid, title}
          })
        const rest_post = await axios.post(post_url, parsedResults)
        console.log(rest_post.data)

    } catch (e) {
        console.log(e)
    }

}

urls.map(url => getWebsiteContent(url))








// const postWebsiteContent = async (job) => {

//     try {
//         await axios.post(post_url, job)

//     } catch (e) {
//         console.log(e)
//     }
// }

// // parsedResults.map(job => postWebsiteContent(job))

// postWebsiteContent(JSON.stringify(parsedResults[0]))


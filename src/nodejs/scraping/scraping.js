const axios = require("axios")
const cheerio = require("cheerio")

const post_url = "http://127.0.0.1:3000/linkedin"
const jobs_url = "https://www.linkedin.com/jobs/view/"

const getJobsContent = async (job_id) => {

    try {
        const res_job = await axios.get(jobs_url + job_id)
        const $ = cheerio.load(res_job.data)
        const title = $(".topcard__title").text()
        const topcard_data = []
        $(".topcard__flavor-row span").map((i,e) => {
            topcard_data.push($(e).text())
        })
        const applicants = $(".num-applicants__caption").text()
        const text = $(".description__text").text()
        $(".job-criteria__list span").map((i,e) => {
            topcard_data.push($(e).text())
        })
        const rest_post = await axios.post(post_url, {
            job_id,
            title,
            company: topcard_data[0],
            location: topcard_data[1],
            posted: topcard_data[2],
            applicants,
            text,
            level: topcard_data[4],
            type: topcard_data[5]
        })
        console.log(rest_post.data)

    } catch (e) {
        console.log(e)
    }

}

module.exports = getJobsContent
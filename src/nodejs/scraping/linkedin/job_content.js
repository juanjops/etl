const axios = require("axios")
const cheerio = require("cheerio")
const C = require("../../constants.js")

const post_url = `http://127.0.0.1:${C.SERVER_PORT}/linkedin`

const getJobContent = async (job_id) => {

    try {
        
        const res_job = await axios.get(C.LINKEDIN_URL + "/jobs/view/" + job_id)
        
        const $ = cheerio.load(res_job.data)
        const title = $(".topcard__title").text()
        const company =  $($(".topcard__flavor-row span")[0]).text()
        const location =  $($(".topcard__flavor-row span")[1]).text()
        const posted =  $($(".topcard__flavor-row span")[2]).text()
        const applicants = $(".num-applicants__caption").text()
        const text = $(".description__text").text()
        const level = $($(".job-criteria__list span")[1]).text()
        const type = $($(".job-criteria__list span")[2]).text()

        await axios.post(post_url, {job_id, title, company, location, posted, applicants, text, level, type})

    } catch (e) {
        console.log(e)
    }

}

module.exports = getJobContent
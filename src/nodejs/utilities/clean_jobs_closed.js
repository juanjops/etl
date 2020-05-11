const axios = require("axios")
const C = require("../constants.js")
const cheerio = require("cheerio")

const COLLECTION_URL = `http://127.0.0.1:${C.SERVER_PORT}/datascience`

const LINKEDIN_URL = "https://www.linkedin.com"

const main = async () => {

    const jobs_avail_aux = []
    try {
        const jobs_id = await get_jobs_id(COLLECTION_URL)
        // const jobs_id = ["1826413957"]
        jobs_id.map(async job_id => {
            jobs_avail_aux.push(getJobAvail(job_id))
        })
        const jobs_avail = await Promise.all(jobs_avail_aux)
        jobs_avail.map(job => patch_job(COLLECTION_URL, job))
    } catch(e) {
        console.log(e)
    }
}

async function get_jobs_id(collection_url) {
    const jobs_id = []
    try {
        const jobs = await axios.get(collection_url)
        jobs.data.forEach(job=> jobs_id.push(job.job_id))
        return jobs_id
    } catch(e) {
        console.log(e)
    }
}

async function getJobAvail(job_id) {

    try {
        const res_job = await axios.get(LINKEDIN_URL + "/jobs/view/" + job_id)
        const $ = cheerio.load(res_job.data)
        const title = $(".apply-button").text()
        if (title === "") {
            return {
                job_id: job_id,
                available: "Not Available"
            }
        } else {
            return {
                job_id: job_id,
                available: "Available"
            }
        }
    } catch(e) {
        console.log("Error in job_id " + job_id)
    }
}

async function patch_job(collection_url, job) {

    try {
        const job_url = collection_url + "/" + job.job_id
        await axios.patch(job_url, job)
        console.log(job)
    } catch(e) {
        console.log(e)
    }
}

main()
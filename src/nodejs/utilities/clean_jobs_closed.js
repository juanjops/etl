const axios = require("axios")
const C = require("../constants.js")
const cheerio = require("cheerio")
const httpProxyAgent = require('http-proxy-agent')
const httpsProxyAgent = require('https-proxy-agent')

const COLLECTION_URL = `http://127.0.0.1:${C.SERVER_PORT}/datasciences`

const COLLECTION_ANALYSIS_URL = `http://127.0.0.1:${C.SERVER_PORT}/datasciences_analysis`

const LINKEDIN_URL = "https://www.linkedin.com"

const agent = new httpProxyAgent(C.PROXY)
// const agent = new httpsProxyAgent("184.75.210.62:80")

const main = async () => {
    
    const jobs_id = await get_jobs_id(COLLECTION_URL)
    console.log(jobs_id.length)

    for (let page_number = 0; page_number < (Math.round(jobs_id.length/100) + 2); page_number++) {
        console.log(page_number)
        let jobs_aux = []
        let jobs_id_partition = jobs_id.slice(page_number*100, page_number*100 + 100)

        try {
            jobs_id_partition.map(async job_id => {
                jobs_aux.push(getJobAvail(job_id))
            })
            let jobs_avail = await Promise.all(jobs_aux)
            jobs_avail.map(job => patch_job(COLLECTION_URL, job))
            jobs_avail.map(job => patch_job(COLLECTION_ANALYSIS_URL, job))
        } catch(e) {
            console.log(e)
        }
        await sleep(1000)
    }

}

async function sleep(miliseconds) {
    return new Promise(resolve => setTimeout(resolve, miliseconds))
}

async function get_jobs_id(collection_url) {
    const jobs_id = []
    try {
        const jobs = await axios.get(collection_url + "/available" + "/Available")
        jobs.data.forEach(job => jobs_id.push(job.job_id))
        return jobs_id
    } catch(e) {
        console.log(e)
    }
}

async function getJobAvail(job_id) {

    try {
        const res_job = await axios.get(
            LINKEDIN_URL + "/jobs/view/" + job_id, {   
                httpAgent: agent
            })
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
        const job_url = collection_url + "/available/" + job.job_id
        await axios.patch(job_url, job)
    } catch(e) {
        console.log(e)
    }
}

main()
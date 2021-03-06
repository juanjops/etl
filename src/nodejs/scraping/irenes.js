const args = require('yargs').argv
const puppeteer = require("puppeteer")
const cheerio = require("cheerio")
const axios = require("axios")
const C = require("../constants.js")
const httpProxyAgent = require('http-proxy-agent')


const JOB_SEARCH_SPECS = {
    "key_words": args.key_words,
    "location" : args.location,
    "time_range": args.time_range
}

const TIMES_PARAMETERS = {
    "Past 24 hours": "r86400",
    "Past Week": "r604800",
    "Past Month": "r2592000",
    "Any Time": ""
}

const SECS = 3

const LINKEDIN_URL = "https://www.linkedin.com"

const post_url = `http://127.0.0.1:${C.SERVER_PORT}/irenes`

const agent = new httpProxyAgent(C.PROXY)

const main = async (jobs_search_specs) => {
    try {
        const jobs_id = await getJobsId(jobs_search_specs)
        console.log("Scraped Jobs: " + jobs_id.length.toString())
        for (let page_number = 0; page_number < (jobs_id.length/100).toFixed(0) + 2; page_number++) {
            let jobs_id_partition = jobs_id.slice(page_number*100, page_number*100 + 100)
            jobs_id_partition.map(job_id => getJobContent(job_id))
            await sleep(500)
        }
    } catch (e) {
        console.log(e)
    }
}

async function sleep(miliseconds) {
    return new Promise(resolve => setTimeout(resolve, miliseconds))
}

const adapt_words = ((str) => {
    return str.replace(/ /g, "%20")
})

const filtered_array = (jobs_id) => {
    return [...new Set(jobs_id.filter( (el) => {return el != null}))]
}

const getJobsId = async (job_search_specs) => {

    jobs_id = []

    try {

        const browser = await puppeteer.launch({headless: true})
        const page = await browser.newPage()
    
        await page.goto(LINKEDIN_URL + "/login")
        await page.type('#username', C.IRENE_USER)
        await page.type('#password', C.IRENE_PASSWORD)
        await page.click(".from__button--floating")
        await page.waitForNavigation()
        for (let page_number = 1; page_number < 40; page_number++) {
            let job_url = (
                LINKEDIN_URL + "/jobs/search/?" + "f_E=2%2C3%2C4" +
                "&f_TPR=" + 
                TIMES_PARAMETERS[job_search_specs["time_range"]] +
                "&keywords=" +
                adapt_words(job_search_specs["key_words"]) + "%2C%20" +
                "&location=" +
                adapt_words(job_search_specs["location"]) + 
                "&start=" + 
                ((page_number-1)*25).toString()
            )
            await page.goto(job_url)
            if (page_number === 1) {
                const jobs_number = await getNumberJobs(page)
                console.log("Jobs Number: " + jobs_number)
            }
            await page.waitFor(1000 * SECS)
            for (let index = 0; index < 400; index++) {await scroll(page)}
            await page.waitFor(1000 * SECS)
            const jobs_id_page = await getHtmlContent(page)
            if (jobs_id_page.length === 0) {
                break
            } else {
                jobs_id = jobs_id.concat(jobs_id_page)
            }
        }
        await browser.close()
    
        return filtered_array(jobs_id)
    } catch (e) {
        console.log(e)
    }

}

async function scroll(page) {
    return page.evaluate(() => {
        document.querySelector('.jobs-search-results').scrollBy(0,10)
    });
}

async function getHtmlContent(page) {
    const jobs_id_page = []
    const html = await page.content()
    const $ = cheerio.load(html)
    $("div[data-job-id]").each((index, element) => {
        jobs_id_page.push($(element).attr("data-job-id").split(":")[3])
    })
    return jobs_id_page
}

async function getNumberJobs(page) {
    const html = await page.content()
    const $ = cheerio.load(html)
    const jobs_number = $("div .jobs-search-two-pane__title-heading small").text().trim().split(" ")[0]
    return jobs_number
}

const getJobContent = async (job_id) => {

    try {
        
        const res_job = await axios.get(
            LINKEDIN_URL + "/jobs/view/" + job_id, {   
                httpAgent: agent
            })
        
        const $ = cheerio.load(res_job.data)
        const title = $(".topcard__title").text()
        const company =  $($(".topcard__flavor-row span")[0]).text()
        const location =  $($(".topcard__flavor-row span")[1]).text()
        const text = $(".description__text").text()
        const level = $($(".job-criteria__list span")[1]).text()
        const type = $($(".job-criteria__list span")[2]).text()
        const link = $(".apply-button").attr("href")

        await axios.post(post_url, {job_id, title, company, location, text, level, type, link})

    } catch (e) {
        console.log("Error in job_id " + job_id)
    }

}

main(JOB_SEARCH_SPECS)

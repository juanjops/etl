const puppeteer = require("puppeteer")
const cheerio = require("cheerio")
const C = require("../../constants.js")

const TIMES_PARAMETERS = {
    "Past 24 hours": "r86400",
    "Past Week": "r604800",
    "Past Month": "r2592000"}

const adapt_words = ((str) => {
    return str.replace(/ /g, "%20")
})

const getJobsId = async (job_search_specs) => {

    jobs_id = []

    try {

        const job_url = (
            C.LINKEDIN_URL + "/jobs/search/?" + "f_E=2%2C3%2C4&" +
            "f_TPR=" + TIMES_PARAMETERS[job_search_specs["time_range"]] +
            "&keywords=" +
            adapt_words(job_search_specs["key_words"]) + "%2C%20" +
            "&location=" +
            adapt_words(job_search_specs["location"])
        )    
        const browser = await puppeteer.launch({headless: false})
        const page = await browser.newPage()
    
        await page.goto(C.LINKEDIN_URL + "/login")
        await page.type('#username', C.USER)
        await page.type('#password', C.PASSWORD)
        await page.click(".from__button--floating")
        await page.waitForNavigation()
        await page.goto(job_url)
        for (let page_number = 1; page_number < 4; page_number++) {
            await page.waitFor(1000)
            for (let index = 0; index < 400; index++) {await scroll(page)}
            await page.waitFor(1000)
            jobs_id = jobs_id.concat(await getHtmlContent(page));
            await page.click(`button[aria-label='Page ${page_number}']`)
        }
        await browser.close()
    
        return [...new Set(jobs_id)]
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

module.exports = getJobsId
const puppeteer = require("puppeteer")
const cheerio = require("cheerio")

const linkedin_url = "https://www.linkedin.com/login"

const job_url = "https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=104738515&keywords=data%20science&location=Ireland"

const getJobsId = async () => {

    jobs_id = []

    try {
        const browser = await puppeteer.launch({headless: false})
        const page = await browser.newPage()
    
        await page.goto(linkedin_url)
        await page.type('#username', "juanjose.pardo.s@gmail.com")
        await page.type('#password', "malekith1990")
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
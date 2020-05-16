
console.log('Client-side code running')

const loadJobs = document.getElementById("Load-Button")
const yesButton = document.getElementById('Yes-Button')
const NoButton = document.getElementById('No-Button')
const text = document.getElementById('text')

const BASE_URL = 'http://localhost:3000/datasciences_analysis/target'
const BASE_URL_TEXT = 'http://localhost:3000/datasciences/text'

loadJobs.addEventListener("click", async (e) => {

  let i = 0
  let job_id = 0

  
  try {

    const jobs = await axios.get(BASE_URL)

    job_id = jobs.data[i].job_id
    let job = await axios.get(BASE_URL_TEXT + "/" + job_id)
    text.textContent = job.data.text

    yesButton.addEventListener("click",async (e) => {
      e.preventDefault()
      await axios.patch(BASE_URL + "/" + job_id, {job_id, target: "YES"})
      i++
      text.textContent = 'Loading...'
      job_id = jobs.data[i].job_id
      let job = await axios.get(BASE_URL_TEXT + "/" + job_id)
      text.textContent = job.data.text
      })
  
    NoButton.addEventListener("click",async (e) => {
      e.preventDefault()
      await axios.patch(BASE_URL +"/" + job_id, {job_id, target: "NO"})
      i++
      text.textContent = 'Loading...'
      job_id = jobs.data[i].job_id
      let job = await axios.get(BASE_URL_TEXT + "/" + job_id)
      text.textContent = job.data.text
      })

  } catch(e) {
    text.textContent = "ERROR - Jobs not loaded"
  }

})

const adapt_words = ((str) => {
  return str.replace(/./g, "\n   \n")
})

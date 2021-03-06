
console.log('Client-side code running')

const loadJobs = document.getElementById("Load-Button")
const yesButton = document.getElementById('Yes-Button')
const NoButton = document.getElementById('No-Button')
const text = document.getElementById('text')
const title = document.getElementById("title")
const company = document.getElementById('company')
const location = document.getElementById('location')
const job_id_number = document.getElementById('job_id')
const key_words = document.getElementById('key_words')
const experience = document.getElementById('experience')
const link = document.getElementById('link')

const BASE_URL = 'http://localhost:3000/datasciences_analysis/target'
const BASE_URL_TEXT = 'http://localhost:3000/datasciences/text'
const BASE_URL_EXPERIENCE = 'http://localhost:3000/datasciences_analysis/experience'

loadJobs.addEventListener("click", async (e) => {

  let i = 0
  let job_id = 0
  
  try {

    const jobs = await axios.get(BASE_URL)

    job_id = jobs.data[i].job_id
    let job_text = await axios.get(BASE_URL_TEXT + "/" + job_id)
    text.textContent = job_text.data.text
    title.textContent = job_text.data.title
    company.textContent = job_text.data.company
    location.textContent = job_text.data.location
    job_id_number.textContent = job_text.data.job_id
    link.textContent = job_text.data.link
    let job_experience = await axios.get(BASE_URL_EXPERIENCE + "/" + job_id)
    key_words.textContent = job_experience.data.key_words
    experience.textContent = job_experience.data.experience

    yesButton.addEventListener("click",async (e) => {
      e.preventDefault()
      await axios.patch(BASE_URL + "/" + job_id, {job_id, target: "YES"})
      i++
      text.textContent = 'Loading...'
      job_id = jobs.data[i].job_id
      let job_text = await axios.get(BASE_URL_TEXT + "/" + job_id)
      text.textContent = job_text.data.text
      title.textContent = job_text.data.title
      company.textContent = job_text.data.company
      location.textContent = job_text.data.location
      job_id_number.textContent = job_text.data.job_id
      link.textContent = job_text.data.link
      let job_experience = await axios.get(BASE_URL_EXPERIENCE + "/" + job_id)
      key_words.textContent = job_experience.data.key_words
      experience.textContent = job_experience.data.experience
      })
  
    NoButton.addEventListener("click",async (e) => {
      e.preventDefault()
      await axios.patch(BASE_URL + "/" + job_id, {job_id, target: "NO"})
      i++
      text.textContent = 'Loading...'
      job_id = jobs.data[i].job_id
      let job_text = await axios.get(BASE_URL_TEXT + "/" + job_id)
      text.textContent = job_text.data.text
      title.textContent = job_text.data.title
      company.textContent = job_text.data.company
      location.textContent = job_text.data.location
      job_id_number.textContent = job_text.data.job_id
      link.textContent = job_text.data.link
      let job_experience = await axios.get(BASE_URL_EXPERIENCE + "/" + job_id)
      key_words.textContent = job_experience.data.key_words
      experience.textContent = job_experience.data.experience
      })

  } catch(e) {
    text.textContent = "ERROR - Jobs not loaded"
  }

})

const adapt_words = ((str) => {
  return str.replace(/./g, "\n   \n")
})

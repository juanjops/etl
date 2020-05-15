
console.log('Client-side code running')

const loadJobs = document.getElementById("Load-Button")
const yesButton = document.getElementById('Yes-Button')
const NoButton = document.getElementById('No-Button')
const text = document.getElementById('text')

const BASE_URL = 'http://localhost:3000/datasciences'

loadJobs.addEventListener("click", async (e) => {

  let i = 0
  let job_id = 0

  try {
    const res = await axios.get(BASE_URL + "/target")
    
    text.textContent = res.data[i].text.replace(/ /g, "\r\n")
    job_id = res.data[i].job_id

    yesButton.addEventListener("click",async (e) => {
      e.preventDefault()
      await axios.patch(BASE_URL + "/target/" + job_id, {job_id, target: "YES"})
      i++
      text.textContent = 'Loading...'
      text.textContent = res.data[i].text
      job_id = res.data[i].job_id
      })
  
    NoButton.addEventListener("click",async (e) => {
      e.preventDefault()
      await axios.patch(BASE_URL + "/target/" + job_id, {job_id, target: "NO"})
      i++
      text.textContent = 'Loading...'
      text.textContent = res.data[i].text
      job_id = res.data[i].job_id
      })

  } catch(e) {
    text.textContent = "ERROR - Jobs not loaded"
  }

})

const adapt_words = ((str) => {
  return str.replace(/./g, "\n   \n")
})

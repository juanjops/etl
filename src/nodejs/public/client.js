const axios = require("axios")
const C = require("../constants.js")
console.log('Client-side code running')

const yesButton = document.getElementById('Yes-Button')
const NoButton = document.getElementById('No-Button');
const text = document.getElementById('text')

const COLLECTION_URL = `http://127.0.0.1:${C.SERVER_PORT}/datascience`

const main = async () => {
  const jobs = await axios.get(COLLECTION_URL)
  const jobs_top = jobs.data.slice(0, 10)
  console.log(jobs_top)
  var ed = 0
  yesButton.addEventListener('click', (e) => {
    text.textContent = jobs_top[ed]
    ed += 1
  })
}

main()




NoButton.addEventListener('click', (e) => {
  e.preventDefault()
  console.log('No button was clicked')
})
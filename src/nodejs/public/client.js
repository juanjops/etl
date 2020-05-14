console.log('Client-side code running')

const yesButton = document.getElementById('Yes-Button')
const NoButton = document.getElementById('No-Button');
const text = document.getElementById('text')

const ar = [5,4,8]
var ed = 0
yesButton.addEventListener('click', (e) => {

  text.textContent = ar[ed]
  ed += 1
})

NoButton.addEventListener('click', (e) => {
  e.preventDefault()
  console.log('No button was clicked')
})
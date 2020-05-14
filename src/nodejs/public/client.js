console.log('Client-side code running')

const yesButton = document.getElementById('Yes-Button');
yesButton.addEventListener('click', function(e) {
  console.log('Yes button was clicked')
})

const NoButton = document.getElementById('No-Button');
NoButton.addEventListener('click', function(e) {
  console.log('No button was clicked')
})
const fs = require("fs")
const csv = require("csv-parser")
const axios = require("axios")
const C = require("../constants.js")

const post_url = `http://127.0.0.1:${C.SERVER_PORT}/linkedin`

const main = async (directory) => {
  try {
    const files = []
    fs.readdirSync(directory).forEach(file => {
      files.push(directory + file)
    })
    console.log(files)
    files.map(file => insert_csv(file))
  } catch (e) {
      console.log("error in main ")
  }
}

async function insert_csv(file) {
  try {
    fs.createReadStream(file)
    .pipe(csv({
    mapValues: ({ header, index, value }) => value.trim()
    }))
    .on('data', (data) => axios.post(post_url, data))
    .on('end', () => {
    console.log("all ok")
  })
  } catch (e) {
    console.log("error in file " + file)
  }
}

module.exports = main

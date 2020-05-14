const express = require("express")
const path = require("path")
const click = require("../models/click.js")
const router = new express.Router()

// router.get('/click', (req, res) => {
//     res.send("<h1>Weather ja</h1>")
//   })

router.get('/click', (req, res) => {
    res.sendFile(path.join(__dirname, "../public/index.html"))
  })

module.exports = router

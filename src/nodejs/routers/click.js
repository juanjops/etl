const express = require("express")
const path = require("path")
const router = new express.Router()

router.get('/clicks', (req, res) => {
    res.sendFile(path.join(__dirname, "../public/index.html"))
  })

module.exports = router

const express = require("express")
const twitter = require("../models/twitter.js")
const router = new express.Router()

router.get("/tweets", async (req, res) => {

    try {
        const tweets = await twitter.find({})
        res.send(tweets)
    } catch (e) {
        res.status(500).send()
    }

})

router.post("/tweets", async (req, res) => {

    try {
        const tweet = await twitter(req.body).save()
        res.status(201).send(tweet)
    } catch (e){
        res.status(400).send(e)
    }

})

module.exports = router

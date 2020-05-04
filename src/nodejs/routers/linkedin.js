const express = require("express")
const Linkedin = require("../models/linkedin.js")
const Play = require("../models/play.js")
const router = new express.Router()


router.post("/linkedin", async (req, res) => {

    try {
        const job = await Linkedin(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})

router.post("/play", async (req, res) => {

    try {
        const job = await Play(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})

router.get("/linkedin", async (req, res) => {

    try {
        const jobs = await Linkedin.find({})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})


router.get("/linkedin/:id", async (req, res) => {


    try {
        const job = await Linkedin.findById(req.params.id)
        if (!job) {
            return res.status(404).send()
        }
        res.send(job)
    } catch (e) {
        res.status(500).send()
    }

})


module.exports = router

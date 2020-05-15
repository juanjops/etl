const express = require("express")
const Marketing = require("../models/marketing.js")
const router = new express.Router()


router.post("/marketings", async (req, res) => {

    try {
        const job = await Marketing(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})


router.get("/marketings", async (req, res) => {

    try {
        const jobs = await Marketing.find({})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})


router.get("/marketings/:id", async (req, res) => {


    try {
        const job = await Marketing.findById(req.params.id)
        if (!job) {
            return res.status(404).send()
        }
        res.send(job)
    } catch (e) {
        res.status(500).send()
    }

})

module.exports = router

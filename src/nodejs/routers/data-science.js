const express = require("express")
const dataScience = require("../models/data-science.js")
const router = new express.Router()


router.post("/dataScience", async (req, res) => {

    try {
        const job = await dataScience(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})


router.get("/dataScience", async (req, res) => {

    try {
        const jobs = await dataScience.find({})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})


router.get("/dataScience/:id", async (req, res) => {


    try {
        const job = await dataScience.findById(req.params.id)
        if (!job) {
            return res.status(404).send()
        }
        res.send(job)
    } catch (e) {
        res.status(500).send()
    }

})


module.exports = router

const express = require("express")
const dataScience = require("../models/data-science.js")
const router = new express.Router()


router.post("/datascience", async (req, res) => {

    try {
        const job = await dataScience(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})

router.patch("/datascience/:job_id", async (req, res) => {
    try {
        const job = await dataScience.updateOne(
            {job_id: req.params.job_id},
            {available: req.body.available},
            {new: true, runValidators: true})
        res.send(job)
    } catch(e) {
        res.status(400).send(e)
    }
})


router.get("/datascience", async (req, res) => {

    try {
        const jobs = await dataScience.find({})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})


router.get("/datascience/:id", async (req, res) => {


    try {
        const job = await dataScience.findById(req.params.job_id)
        if (!job) {
            return res.status(404).send()
        }
        res.send(job)
    } catch (e) {
        res.status(500).send()
    }

})


module.exports = router

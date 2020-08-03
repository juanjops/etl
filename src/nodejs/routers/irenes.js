const express = require("express")
const {irenes} = require("../models/irenes.js")
const router = new express.Router()

router.get("/irenes", async (req, res) => {

    try {
        const jobs = await irenes.find({})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})

router.post("/irenes", async (req, res) => {

    try {
        const job = await irenes(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})

router.get("/irenes/:id", async (req, res) => {


    try {
        console.log(req.params.id)
        const job = await irenes.findById(req.params.id)
        if (!job) {
            return res.status(404).send()
        }
        res.send(job)
    } catch (e) {
        res.status(500).send()
    }

})

module.exports = router
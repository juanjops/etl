const express = require("express")
const {dataScience, dataScience_analysis} = require("../models/datasciences.js")
const router = new express.Router()

router.get("/datasciences", async (req, res) => {

    try {
        const jobs = await dataScience.find({})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})

router.post("/datasciences", async (req, res) => {

    try {
        const job = await dataScience(req.body).save()
        res.status(201).send(job)
    } catch (e){
        res.status(400).send(e)
    }

})

router.get("/datasciences/:id", async (req, res) => {


    try {
        console.log(req.params.id)
        const job = await dataScience.findById(req.params.id)
        if (!job) {
            return res.status(404).send()
        }
        res.send(job)
    } catch (e) {
        res.status(500).send()
    }

})

router.get("/datasciences/text/:job_id", async (req, res) => {

    try {
        const jobs = await dataScience.findOne(
            {job_id: req.params.job_id})
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})

router.patch("/datasciences/available/:job_id", async (req, res) => {
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

router.get("/datasciences/available/:available", async (req, res) => {

    try {
        const jobs = await dataScience.find(
            {available: req.params.available},
            "job_id available"
            )
        res.send(jobs)
    } catch (e) {
        res.status(500).send()
    }

})

router.get("/datasciences_analysis/target", async (req, res) => {

    try {
        const jobs = await dataScience_analysis.find(
            {target: {$eq: null}},
            null,
            {limit: 25,
            sort: {available:1, ML: -1, Math: -1, BI: -1, Big_D: -1, CI_CD: -1, Serv: -1}})
        res.send(jobs)
    } catch (e) {
        res.status(400).send()
    }

})

router.patch("/datasciences_analysis/target/:job_id", async (req, res) => {
    try {
        const job = await dataScience_analysis.updateOne(
            {job_id: req.params.job_id},
            {target: req.body.target},
            {new: true, runValidators: true})
        res.send(job)
    } catch(e) {
        res.status(400).send(e)
    }
})

module.exports = router

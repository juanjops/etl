const mongoose = require("mongoose")

const dataScience = mongoose.model("datasciences", {

    job_id: {
        type: String,
        required : true,
        trim: true
    },
    title: {
        type: String,
        trim: true
    },
    company: {
        type: String,
        trim: true
    },
    location: {
        type: String,
        trim: true
    },
    posted: {
        type: Date,
        default: Date.now
    },
    text: {
        type: String,
        trim: true
    },
    level: {
        type: String,
        trim: true
    },
    type: {
        type: String,
        trim: true
    },
    available: {
        type: String,
        trim: true,
        default: "Available"
    },
    target: {
        type: String,
        trim: true
    }
})


module.exports = dataScience
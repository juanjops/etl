const mongoose = require("mongoose")

const Linkedin = mongoose.model("linkedin", {

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
        type: String,
        trim: true
    },
    applicants: {
        type: String,
        trim: true
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
    }
})


module.exports = Linkedin
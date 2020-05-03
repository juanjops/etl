const mongoose = require("mongoose")
const validator = require("validator")

const Linkedin = mongoose.model("linkedin", {

    job_id: {
        type: String,
        required : true,
        trim: true
    },
    title: {
        type: String
    },
    company: {
        type: String
    },
    location: {
        type: String
    },
    posted: {
        type: String
    },
    applicants: {
        type: String
    },
    text: {
        type: String
    },
    level: {
        type: String
    },
    type: {
        type: String
    }
})


module.exports = Linkedin
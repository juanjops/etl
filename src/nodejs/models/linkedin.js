const mongoose = require("mongoose")
const validator = require("validator")


const Linkedin = mongoose.model("linkedin", {

    jobid: {
        type: String,
        required : true,
        trim: true
    },
    title: {
        type: String
    }
    
})


module.exports = Linkedin
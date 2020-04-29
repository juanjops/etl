const mongoose = require("mongoose")
const validator = require("validator")


const Linkedin = mongoose.model("linkedin", {

    jobid: {
        type: String,
        required : true,
        trim: true,
        validate(value) {
            if (!validator.isInt(value)) {
                throw new Error ("job id must be a integer")
            }
        }
    },
    title: {
        type: String
    }
    
})


module.exports = Linkedin